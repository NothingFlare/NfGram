/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.extractor.wav;

/** Format information for a WAV file. */
/* package */ final class WavFormat {

  /**
   * The format type. Standard format types are the "WAVE form Registration Number" constants
   * defined in RFC 2361 Appendix A.
   */
  public final int formatType;
  /** The number of channels. */
  public final int numChannels;
  /** The sample rate in Hertz. */
  public final int frameRateHz;
  /** The average bytes per second for the sample data. */
  public final int averageBytesPerSecond;
  /** The block size in bytes. */
  public final int blockSize;
  /** Bits per sample for a single channel. */
  public final int bitsPerSample;
  /** Extra data appended to the format chunk. */
  public final byte[] extraData;

  public WavFormat(
      int formatType,
      int numChannels,
      int frameRateHz,
      int averageBytesPerSecond,
      int blockSize,
      int bitsPerSample,
      byte[] extraData) {
    this.formatType = formatType;
    this.numChannels = numChannels;
    this.frameRateHz = frameRateHz;
    this.averageBytesPerSecond = averageBytesPerSecond;
    this.blockSize = blockSize;
    this.bitsPerSample = bitsPerSample;
    this.extraData = extraData;
  }
}
