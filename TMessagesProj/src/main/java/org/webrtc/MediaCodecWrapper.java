/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import android.media.MediaCodec;
import android.media.MediaCrypto;
import android.media.MediaFormat;
import android.os.Bundle;
import android.view.Surface;
import java.nio.ByteBuffer;

/**
 * Subset of methods defined in {@link android.media.MediaCodec} needed by
 * {@link HardwareVideoEncoder} and {@link AndroidVideoDecoder}. This interface
 * exists to allow mocking and using a fake implementation in tests.
 */
interface MediaCodecWrapper {
  void configure(MediaFormat format, Surface surface, MediaCrypto crypto, int flags);

  void start();

  void flush();

  void stop();

  void release();

  int dequeueInputBuffer(long timeoutUs);

  void queueInputBuffer(int index, int offset, int size, long presentationTimeUs, int flags);

  int dequeueOutputBuffer(MediaCodec.BufferInfo info, long timeoutUs);

  void releaseOutputBuffer(int index, boolean render);

  MediaFormat getOutputFormat();

  ByteBuffer[] getInputBuffers();

  ByteBuffer[] getOutputBuffers();

  Surface createInputSurface();

  void setParameters(Bundle params);
}
