/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

/**
 * Creates a native {@code webrtc::AudioDecoderFactory} with the builtin audio decoders.
 */
public class BuiltinAudioDecoderFactoryFactory implements AudioDecoderFactoryFactory {
  @Override
  public long createNativeAudioDecoderFactory() {
    return nativeCreateBuiltinAudioDecoderFactory();
  }

  private static native long nativeCreateBuiltinAudioDecoderFactory();
}
