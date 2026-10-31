/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source;

import static com.google.android.exoplayer2.source.mediaparser.MediaParserUtil.PARAMETER_EAGERLY_EXPOSE_TRACK_TYPE;
import static com.google.android.exoplayer2.source.mediaparser.MediaParserUtil.PARAMETER_INCLUDE_SUPPLEMENTAL_DATA;
import static com.google.android.exoplayer2.source.mediaparser.MediaParserUtil.PARAMETER_IN_BAND_CRYPTO_INFO;

import android.annotation.SuppressLint;
import android.media.MediaParser;
import android.media.MediaParser.SeekPoint;
import android.net.Uri;
import android.util.Pair;
import androidx.annotation.RequiresApi;
import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.analytics.PlayerId;
import com.google.android.exoplayer2.extractor.Extractor;
import com.google.android.exoplayer2.extractor.ExtractorOutput;
import com.google.android.exoplayer2.extractor.PositionHolder;
import com.google.android.exoplayer2.source.mediaparser.InputReaderAdapterV30;
import com.google.android.exoplayer2.source.mediaparser.MediaParserUtil;
import com.google.android.exoplayer2.source.mediaparser.OutputConsumerAdapterV30;
import com.google.android.exoplayer2.upstream.DataReader;
import com.google.android.exoplayer2.util.Util;
import java.io.IOException;
import java.util.List;
import java.util.Map;

/** {@link ProgressiveMediaExtractor} implemented on top of the platform's {@link MediaParser}. */
@RequiresApi(30)
public final class MediaParserExtractorAdapter implements ProgressiveMediaExtractor {

  /**
   * A {@link ProgressiveMediaExtractor.Factory} for instances of this class, which rely on platform
   * extractors through {@link MediaParser}.
   */
  public static final ProgressiveMediaExtractor.Factory FACTORY = MediaParserExtractorAdapter::new;

  private final OutputConsumerAdapterV30 outputConsumerAdapter;
  private final InputReaderAdapterV30 inputReaderAdapter;
  private final MediaParser mediaParser;
  private String parserName;

  @SuppressLint("WrongConstant")
  public MediaParserExtractorAdapter(PlayerId playerId) {
    // TODO: Add support for injecting the desired extractor list.
    outputConsumerAdapter = new OutputConsumerAdapterV30();
    inputReaderAdapter = new InputReaderAdapterV30();
    mediaParser = MediaParser.create(outputConsumerAdapter);
    mediaParser.setParameter(PARAMETER_EAGERLY_EXPOSE_TRACK_TYPE, true);
    mediaParser.setParameter(PARAMETER_IN_BAND_CRYPTO_INFO, true);
    mediaParser.setParameter(PARAMETER_INCLUDE_SUPPLEMENTAL_DATA, true);
    parserName = MediaParser.PARSER_NAME_UNKNOWN;
    if (Util.SDK_INT >= 31) {
      MediaParserUtil.setLogSessionIdOnMediaParser(mediaParser, playerId);
    }
  }

  @Override
  public void init(
      DataReader dataReader,
      Uri uri,
      Map<String, List<String>> responseHeaders,
      long position,
      long length,
      ExtractorOutput output)
      throws IOException {
    outputConsumerAdapter.setExtractorOutput(output);
    inputReaderAdapter.setDataReader(dataReader, length);
    inputReaderAdapter.setCurrentPosition(position);
    String currentParserName = mediaParser.getParserName();
    if (MediaParser.PARSER_NAME_UNKNOWN.equals(currentParserName)) {
      // We need to sniff.
      mediaParser.advance(inputReaderAdapter);
      parserName = mediaParser.getParserName();
      outputConsumerAdapter.setSelectedParserName(parserName);
    } else if (!currentParserName.equals(parserName)) {
      // The parser was created by name.
      parserName = mediaParser.getParserName();
      outputConsumerAdapter.setSelectedParserName(parserName);
    } else {
      // The parser implementation has already been selected. Do nothing.
    }
  }

  @Override
  public void release() {
    mediaParser.release();
  }

  @Override
  public void disableSeekingOnMp3Streams() {
    if (MediaParser.PARSER_NAME_MP3.equals(parserName)) {
      outputConsumerAdapter.disableSeeking();
    }
  }

  @Override
  public long getCurrentInputPosition() {
    return inputReaderAdapter.getPosition();
  }

  @Override
  public void seek(long position, long seekTimeUs) {
    inputReaderAdapter.setCurrentPosition(position);
    Pair<SeekPoint, SeekPoint> seekPoints = outputConsumerAdapter.getSeekPoints(seekTimeUs);
    mediaParser.seek(seekPoints.second.position == position ? seekPoints.second : seekPoints.first);
  }

  @Override
  public int read(PositionHolder positionHolder) throws IOException {
    boolean shouldContinue = mediaParser.advance(inputReaderAdapter);
    positionHolder.position = inputReaderAdapter.getAndResetSeekPosition();
    return !shouldContinue
        ? Extractor.RESULT_END_OF_INPUT
        : positionHolder.position != C.POSITION_UNSET
            ? Extractor.RESULT_SEEK
            : Extractor.RESULT_CONTINUE;
  }
}
