/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * This class creates a native {@code webrtc::AudioEncoderFactory} with the builtin audio encoders.
 */
public class BuiltinAudioEncoderFactoryFactory implements AudioEncoderFactoryFactory {
  @Override
  public long createNativeAudioEncoderFactory() {
    return nativeCreateBuiltinAudioEncoderFactory();
  }

  private static native long nativeCreateBuiltinAudioEncoderFactory();
}
