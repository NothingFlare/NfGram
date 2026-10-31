/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.extractor.mp3;

import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.audio.MpegAudioUtil;
import com.google.android.exoplayer2.extractor.ConstantBitrateSeekMap;

/**
 * MP3 seeker that doesn't rely on metadata and seeks assuming the source has a constant bitrate.
 */
/* package */ final class ConstantBitrateSeeker extends ConstantBitrateSeekMap implements Seeker {

  /**
   * @param inputLength The length of the stream in bytes, or {@link C#LENGTH_UNSET} if unknown.
   * @param firstFramePosition The position of the first frame in the stream.
   * @param mpegAudioHeader The MPEG audio header associated with the first frame.
   * @param allowSeeksIfLengthUnknown Whether to allow seeking even if the length of the content is
   *     unknown.
   */
  public ConstantBitrateSeeker(
      long inputLength,
      long firstFramePosition,
      MpegAudioUtil.Header mpegAudioHeader,
      boolean allowSeeksIfLengthUnknown) {
    // Set the seeker frame size to the size of the first frame (even though some constant bitrate
    // streams have variable frame sizes) to avoid the need to re-synchronize for constant frame
    // size streams.
    super(
        inputLength,
        firstFramePosition,
        mpegAudioHeader.bitrate,
        mpegAudioHeader.frameSize,
        allowSeeksIfLengthUnknown);
  }

  @Override
  public long getTimeUs(long position) {
    return getTimeUsAtPosition(position);
  }

  @Override
  public long getDataEndPosition() {
    return C.POSITION_UNSET;
  }
}
