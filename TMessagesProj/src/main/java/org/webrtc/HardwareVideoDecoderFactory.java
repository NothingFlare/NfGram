/*
 * Copyright (C) The WebRTC project authors. All Rights Reserved
 *
 * Licensed under GNU GPLv3.
 */

package org.webrtc;

import android.media.MediaCodecInfo;

import org.telegram.messenger.voip.Instance;
import org.telegram.messenger.voip.VoIPService;

import androidx.annotation.Nullable;

/** Factory for Android hardware VideoDecoders. */
public class HardwareVideoDecoderFactory extends MediaCodecVideoDecoderFactory {
  private final static Predicate<MediaCodecInfo> defaultAllowedPredicate =
      new Predicate<MediaCodecInfo>() {
        @Override
        public boolean test(MediaCodecInfo arg) {
            if (!MediaCodecUtils.isHardwareAccelerated(arg)) {
                return false;
            }
            String[] types = arg.getSupportedTypes();
            if (types == null || types.length == 0) {
                return false;
            }
            Instance.ServerConfig config = Instance.getGlobalServerConfig();
            for (int a = 0; a < types.length; a++) {
                switch (types[a]) {
                    case "video/x-vnd.on2.vp8":
                        if (VoIPService.getSharedInstance() != null && VoIPService.getSharedInstance().groupCall != null) {
                            return false;
                        }
                        return config.enable_vp8_decoder;
                    case "video/x-vnd.on2.vp9":
                        return config.enable_vp9_decoder;
                    case "video/avc":
                        if (VoIPService.getSharedInstance() != null && VoIPService.getSharedInstance().groupCall != null) {
                            return false;
                        }
                        return config.enable_h264_decoder;
                    case "video/hevc":
                        return config.enable_h265_decoder;
                }
            }
            return true;
        }
      };

  /** Creates a HardwareVideoDecoderFactory that does not use surface textures. */
  @Deprecated // Not removed yet to avoid breaking callers.
  public HardwareVideoDecoderFactory() {
    this(null);
  }

  /**
   * Creates a HardwareVideoDecoderFactory that supports surface texture rendering.
   *
   * @param sharedContext The textures generated will be accessible from this context. May be null,
   *                      this disables texture support.
   */
  public HardwareVideoDecoderFactory(@Nullable EglBase.Context sharedContext) {
    this(sharedContext, /* codecAllowedPredicate= */ null);
  }

  /**
   * Creates a HardwareVideoDecoderFactory that supports surface texture rendering.
   *
   * @param sharedContext The textures generated will be accessible from this context. May be null,
   *                      this disables texture support.
   * @param codecAllowedPredicate predicate to filter codecs. It is combined with the default
   *                              predicate that only allows hardware codecs.
   */
  public HardwareVideoDecoderFactory(@Nullable EglBase.Context sharedContext,
      @Nullable Predicate<MediaCodecInfo> codecAllowedPredicate) {
    super(sharedContext,
        (codecAllowedPredicate == null ? defaultAllowedPredicate
                                       : codecAllowedPredicate.and(defaultAllowedPredicate)));
  }
}
