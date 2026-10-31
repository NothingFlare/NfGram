/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import androidx.annotation.Nullable;

/**
 * Lightweight abstraction for an object that can receive video frames, process them, and pass them
 * on to another object. This object is also allowed to observe capturer start/stop.
 */
public interface VideoProcessor extends CapturerObserver {
  public static class FrameAdaptationParameters {
    public final int cropX;
    public final int cropY;
    public final int cropWidth;
    public final int cropHeight;
    public final int scaleWidth;
    public final int scaleHeight;
    public final long timestampNs;
    public final boolean drop;

    public FrameAdaptationParameters(int cropX, int cropY, int cropWidth, int cropHeight,
        int scaleWidth, int scaleHeight, long timestampNs, boolean drop) {
      this.cropX = cropX;
      this.cropY = cropY;
      this.cropWidth = cropWidth;
      this.cropHeight = cropHeight;
      this.scaleWidth = scaleWidth;
      this.scaleHeight = scaleHeight;
      this.timestampNs = timestampNs;
      this.drop = drop;
    }
  }

  /**
   * This is a chance to access an unadapted frame. The default implementation applies the
   * adaptation and forwards the frame to {@link #onFrameCaptured(VideoFrame)}.
   */
  default void onFrameCaptured(VideoFrame frame, FrameAdaptationParameters parameters) {
    VideoFrame adaptedFrame = applyFrameAdaptationParameters(frame, parameters);
    if (adaptedFrame != null) {
      onFrameCaptured(adaptedFrame);
      adaptedFrame.release();
    }
  }

  /**
   * Set the sink that receives the output from this processor. Null can be passed in to unregister
   * a sink.
   */
  void setSink(@Nullable VideoSink sink);

  /**
   * Applies the frame adaptation parameters to a frame. Returns null if the frame is meant to be
   * dropped. Returns a new frame. The caller is responsible for releasing the returned frame.
   */
  public static @Nullable VideoFrame applyFrameAdaptationParameters(
      VideoFrame frame, FrameAdaptationParameters parameters) {
    if (parameters.drop) {
      return null;
    }

    final VideoFrame.Buffer adaptedBuffer =
        frame.getBuffer().cropAndScale(parameters.cropX, parameters.cropY, parameters.cropWidth,
            parameters.cropHeight, parameters.scaleWidth, parameters.scaleHeight);
    return new VideoFrame(adaptedBuffer, frame.getRotation(), parameters.timestampNs);
  }
}
