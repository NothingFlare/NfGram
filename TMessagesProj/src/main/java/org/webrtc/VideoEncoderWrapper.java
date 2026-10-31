/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

// Explicit imports necessary for JNI generation.
import androidx.annotation.Nullable;
import org.webrtc.VideoEncoder;

/**
 * This class contains the Java glue code for JNI generation of VideoEncoder.
 */
class VideoEncoderWrapper {
  @CalledByNative
  static boolean getScalingSettingsOn(VideoEncoder.ScalingSettings scalingSettings) {
    return scalingSettings.on;
  }

  @Nullable
  @CalledByNative
  static Integer getScalingSettingsLow(VideoEncoder.ScalingSettings scalingSettings) {
    return scalingSettings.low;
  }

  @Nullable
  @CalledByNative
  static Integer getScalingSettingsHigh(VideoEncoder.ScalingSettings scalingSettings) {
    return scalingSettings.high;
  }

  @CalledByNative
  static VideoEncoder.Callback createEncoderCallback(final long nativeEncoder) {
    return (EncodedImage frame,
               VideoEncoder.CodecSpecificInfo info) -> nativeOnEncodedFrame(nativeEncoder, frame);
  }

  private static native void nativeOnEncodedFrame(
      long nativeVideoEncoderWrapper, EncodedImage frame);
}
