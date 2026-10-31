/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.text;

import com.google.android.exoplayer2.decoder.Decoder;

/** Decodes {@link Subtitle}s from {@link SubtitleInputBuffer}s. */
public interface SubtitleDecoder
    extends Decoder<SubtitleInputBuffer, SubtitleOutputBuffer, SubtitleDecoderException> {

  /**
   * Informs the decoder of the current playback position.
   *
   * <p>Must be called prior to each attempt to dequeue output buffers from the decoder.
   *
   * @param positionUs The current playback position in microseconds.
   */
  void setPositionUs(long positionUs);
}
