/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.extractor.ts;

import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.Format;
import com.google.android.exoplayer2.extractor.ExtractorOutput;
import com.google.android.exoplayer2.extractor.TrackOutput;
import com.google.android.exoplayer2.util.Assertions;
import com.google.android.exoplayer2.util.ParsableByteArray;
import com.google.android.exoplayer2.util.TimestampAdjuster;
import com.google.android.exoplayer2.util.Util;
import org.checkerframework.checker.nullness.qual.EnsuresNonNull;
import org.checkerframework.checker.nullness.qual.MonotonicNonNull;

/**
 * A {@link SectionPayloadReader} that directly outputs the section bytes as sample data.
 *
 * <p>Timestamp adjustment is provided through {@link Format#subsampleOffsetUs}.
 */
public final class PassthroughSectionPayloadReader implements SectionPayloadReader {

  private Format format;
  private @MonotonicNonNull TimestampAdjuster timestampAdjuster;
  private @MonotonicNonNull TrackOutput output;

  /**
   * Create a new PassthroughSectionPayloadReader.
   *
   * @param mimeType The MIME type set as {@link Format#sampleMimeType} on the created output track.
   */
  public PassthroughSectionPayloadReader(String mimeType) {
    this.format = new Format.Builder().setSampleMimeType(mimeType).build();
  }

  @Override
  public void init(
      TimestampAdjuster timestampAdjuster,
      ExtractorOutput extractorOutput,
      TsPayloadReader.TrackIdGenerator idGenerator) {
    this.timestampAdjuster = timestampAdjuster;
    idGenerator.generateNewId();
    output = extractorOutput.track(idGenerator.getTrackId(), C.TRACK_TYPE_METADATA);
    // Eagerly output an incomplete format (missing timestamp offset) to ensure source preparation
    // is not blocked waiting for potentially sparse metadata.
    output.format(format);
  }

  @Override
  public void consume(ParsableByteArray sectionData) {
    assertInitialized();
    long sampleTimestampUs = timestampAdjuster.getLastAdjustedTimestampUs();
    long subsampleOffsetUs = timestampAdjuster.getTimestampOffsetUs();
    if (sampleTimestampUs == C.TIME_UNSET || subsampleOffsetUs == C.TIME_UNSET) {
      // Don't output samples without a known sample timestamp and subsample offset.
      return;
    }
    if (subsampleOffsetUs != format.subsampleOffsetUs) {
      format = format.buildUpon().setSubsampleOffsetUs(subsampleOffsetUs).build();
      output.format(format);
    }
    int sampleSize = sectionData.bytesLeft();
    output.sampleData(sectionData, sampleSize);
    output.sampleMetadata(sampleTimestampUs, C.BUFFER_FLAG_KEY_FRAME, sampleSize, 0, null);
  }

  @EnsuresNonNull({"timestampAdjuster", "output"})
  private void assertInitialized() {
    Assertions.checkStateNotNull(timestampAdjuster);
    Util.castNonNull(output);
  }
}
