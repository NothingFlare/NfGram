/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.hls;

import android.net.Uri;
import androidx.annotation.Nullable;
import com.google.android.exoplayer2.Format;
import com.google.android.exoplayer2.analytics.PlayerId;
import com.google.android.exoplayer2.extractor.Extractor;
import com.google.android.exoplayer2.extractor.ExtractorInput;
import com.google.android.exoplayer2.extractor.PositionHolder;
import com.google.android.exoplayer2.util.TimestampAdjuster;
import java.io.IOException;
import java.util.List;
import java.util.Map;

/** Factory for HLS media chunk extractors. */
public interface HlsExtractorFactory {

  HlsExtractorFactory DEFAULT = new DefaultHlsExtractorFactory();

  /**
   * Creates an {@link Extractor} for extracting HLS media chunks.
   *
   * @param uri The URI of the media chunk.
   * @param format A {@link Format} associated with the chunk to extract.
   * @param muxedCaptionFormats List of muxed caption {@link Format}s. Null if no closed caption
   *     information is available in the multivariant playlist.
   * @param timestampAdjuster Adjuster corresponding to the provided discontinuity sequence number.
   * @param responseHeaders The HTTP response headers associated with the media segment or
   *     initialization section to extract.
   * @param sniffingExtractorInput The first extractor input that will be passed to the returned
   *     extractor's {@link Extractor#read(ExtractorInput, PositionHolder)}. Must only be used to
   *     call {@link Extractor#sniff(ExtractorInput)}.
   * @param playerId The {@link PlayerId} of the player using this extractors factory.
   * @return An {@link HlsMediaChunkExtractor}.
   * @throws IOException If an I/O error is encountered while sniffing.
   */
  HlsMediaChunkExtractor createExtractor(
      Uri uri,
      Format format,
      @Nullable List<Format> muxedCaptionFormats,
      TimestampAdjuster timestampAdjuster,
      Map<String, List<String>> responseHeaders,
      ExtractorInput sniffingExtractorInput,
      PlayerId playerId)
      throws IOException;
}
