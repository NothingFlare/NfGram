/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.drm;

import com.google.android.exoplayer2.drm.ExoMediaDrm.KeyRequest;
import com.google.android.exoplayer2.drm.ExoMediaDrm.ProvisionRequest;
import com.google.android.exoplayer2.util.Assertions;
import java.util.UUID;

/**
 * A {@link MediaDrmCallback} that provides a fixed response to key requests. Provisioning is not
 * supported. This implementation is primarily useful for providing locally stored keys to decrypt
 * ClearKey protected content. It is not suitable for use with Widevine or PlayReady protected
 * content.
 */
public final class LocalMediaDrmCallback implements MediaDrmCallback {

  private final byte[] keyResponse;

  /**
   * @param keyResponse The fixed response for all key requests.
   */
  public LocalMediaDrmCallback(byte[] keyResponse) {
    this.keyResponse = Assertions.checkNotNull(keyResponse);
  }

  @Override
  public byte[] executeProvisionRequest(UUID uuid, ProvisionRequest request) {
    throw new UnsupportedOperationException();
  }

  @Override
  public byte[] executeKeyRequest(UUID uuid, KeyRequest request) {
    return keyResponse;
  }
}
