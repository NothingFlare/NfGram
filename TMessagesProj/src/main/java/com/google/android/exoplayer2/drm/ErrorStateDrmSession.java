/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.drm;

import androidx.annotation.Nullable;
import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.decoder.CryptoConfig;
import com.google.android.exoplayer2.util.Assertions;
import java.util.Map;
import java.util.UUID;

/** A {@link DrmSession} that's in a terminal error state. */
public final class ErrorStateDrmSession implements DrmSession {

  private final DrmSessionException error;

  public ErrorStateDrmSession(DrmSessionException error) {
    this.error = Assertions.checkNotNull(error);
  }

  @Override
  public int getState() {
    return STATE_ERROR;
  }

  @Override
  public boolean playClearSamplesWithoutKeys() {
    return false;
  }

  @Override
  @Nullable
  public DrmSessionException getError() {
    return error;
  }

  @Override
  public final UUID getSchemeUuid() {
    return C.UUID_NIL;
  }

  @Override
  @Nullable
  public CryptoConfig getCryptoConfig() {
    return null;
  }

  @Override
  @Nullable
  public Map<String, String> queryKeyStatus() {
    return null;
  }

  @Override
  @Nullable
  public byte[] getOfflineLicenseKeySetId() {
    return null;
  }

  @Override
  public boolean requiresSecureDecoder(String mimeType) {
    return false;
  }

  @Override
  public void acquire(@Nullable DrmSessionEventListener.EventDispatcher eventDispatcher) {
    // Do nothing.
  }

  @Override
  public void release(@Nullable DrmSessionEventListener.EventDispatcher eventDispatcher) {
    // Do nothing.
  }
}
