/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.extractor.ts;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.Format;
import com.google.android.exoplayer2.extractor.CeaUtil;
import com.google.android.exoplayer2.extractor.ExtractorOutput;
import com.google.android.exoplayer2.extractor.TrackOutput;
import com.google.android.exoplayer2.extractor.ts.TsPayloadReader.TrackIdGenerator;
import com.google.android.exoplayer2.util.Assertions;
import com.google.android.exoplayer2.util.MimeTypes;
import com.google.android.exoplayer2.util.ParsableByteArray;
import java.util.List;

/** Consumes SEI buffers, outputting contained CEA-608/708 messages to a {@link TrackOutput}. */
public final class SeiReader {

  private final List<Format> closedCaptionFormats;
  private final TrackOutput[] outputs;

  /**
   * @param closedCaptionFormats A list of formats for the closed caption channels to expose.
   */
  public SeiReader(List<Format> closedCaptionFormats) {
    this.closedCaptionFormats = closedCaptionFormats;
    outputs = new TrackOutput[closedCaptionFormats.size()];
  }

  public void createTracks(ExtractorOutput extractorOutput, TrackIdGenerator idGenerator) {
    for (int i = 0; i < outputs.length; i++) {
      idGenerator.generateNewId();
      TrackOutput output = extractorOutput.track(idGenerator.getTrackId(), C.TRACK_TYPE_TEXT);
      Format channelFormat = closedCaptionFormats.get(i);
      @Nullable String channelMimeType = channelFormat.sampleMimeType;
      Assertions.checkArgument(
          MimeTypes.APPLICATION_CEA608.equals(channelMimeType)
              || MimeTypes.APPLICATION_CEA708.equals(channelMimeType),
          "Invalid closed caption mime type provided: " + channelMimeType);
      String formatId = channelFormat.id != null ? channelFormat.id : idGenerator.getFormatId();
      output.format(
          new Format.Builder()
              .setId(formatId)
              .setSampleMimeType(channelMimeType)
              .setSelectionFlags(channelFormat.selectionFlags)
              .setLanguage(channelFormat.language)
              .setAccessibilityChannel(channelFormat.accessibilityChannel)
              .setInitializationData(channelFormat.initializationData)
              .build());
      outputs[i] = output;
    }
  }

  public void consume(long pesTimeUs, ParsableByteArray seiBuffer) {
    CeaUtil.consume(pesTimeUs, seiBuffer, outputs);
  }
}
