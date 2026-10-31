/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import android.media.MediaCodecInfo;
import androidx.annotation.Nullable;
import java.util.Arrays;

/** Factory for Android platform software VideoDecoders. */
public class PlatformSoftwareVideoDecoderFactory extends MediaCodecVideoDecoderFactory {
  /**
   * Default allowed predicate.
   */
  private static final Predicate<MediaCodecInfo> defaultAllowedPredicate =
      new Predicate<MediaCodecInfo>() {
        @Override
        public boolean test(MediaCodecInfo arg) {
          return MediaCodecUtils.isSoftwareOnly(arg);
        }
      };

  /**
   * Creates a PlatformSoftwareVideoDecoderFactory that supports surface texture rendering.
   *
   * @param sharedContext The textures generated will be accessible from this context. May be null,
   *                      this disables texture support.
   */
  public PlatformSoftwareVideoDecoderFactory(@Nullable EglBase.Context sharedContext) {
    super(sharedContext, defaultAllowedPredicate);
  }
}
