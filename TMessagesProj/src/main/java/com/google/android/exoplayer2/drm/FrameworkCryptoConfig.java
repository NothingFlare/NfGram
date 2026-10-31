/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.drm;

import android.media.MediaCodec;
import android.media.MediaCrypto;
import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.decoder.CryptoConfig;
import com.google.android.exoplayer2.util.Util;
import java.util.UUID;

/**
 * A {@link CryptoConfig} for {@link C#CRYPTO_TYPE_FRAMEWORK}. Contains the necessary information to
 * build or update a framework {@link MediaCrypto} that can be used to configure a {@link
 * MediaCodec}.
 */
public final class FrameworkCryptoConfig implements CryptoConfig {

  /**
   * Whether the device needs keys to have been loaded into the {@link DrmSession} before codec
   * configuration.
   */
  public static final boolean WORKAROUND_DEVICE_NEEDS_KEYS_TO_CONFIGURE_CODEC =
      "Amazon".equals(Util.MANUFACTURER)
          && ("AFTM".equals(Util.MODEL) // Fire TV Stick Gen 1
              || "AFTB".equals(Util.MODEL)); // Fire TV Gen 1

  /** The DRM scheme UUID. */
  public final UUID uuid;
  /** The DRM session id. */
  public final byte[] sessionId;
  /**
   * Whether to allow use of insecure decoder components even if the underlying platform says
   * otherwise.
   */
  public final boolean forceAllowInsecureDecoderComponents;

  /**
   * @param uuid The DRM scheme UUID.
   * @param sessionId The DRM session id.
   * @param forceAllowInsecureDecoderComponents Whether to allow use of insecure decoder components
   *     even if the underlying platform says otherwise.
   */
  public FrameworkCryptoConfig(
      UUID uuid, byte[] sessionId, boolean forceAllowInsecureDecoderComponents) {
    this.uuid = uuid;
    this.sessionId = sessionId;
    this.forceAllowInsecureDecoderComponents = forceAllowInsecureDecoderComponents;
  }
}
