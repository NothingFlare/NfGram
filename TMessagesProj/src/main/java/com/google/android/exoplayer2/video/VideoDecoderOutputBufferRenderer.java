/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.video;

import com.google.android.exoplayer2.decoder.VideoDecoderOutputBuffer;

/** Renders the {@link VideoDecoderOutputBuffer}. */
public interface VideoDecoderOutputBufferRenderer {

  /**
   * Sets the output buffer to be rendered. The renderer is responsible for releasing the buffer.
   *
   * @param outputBuffer The output buffer to be rendered.
   */
  void setOutputBuffer(VideoDecoderOutputBuffer outputBuffer);
}
