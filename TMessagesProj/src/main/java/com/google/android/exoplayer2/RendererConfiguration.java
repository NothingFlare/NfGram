/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2;

import androidx.annotation.Nullable;

/** The configuration of a {@link Renderer}. */
public final class RendererConfiguration {

  /** The default configuration. */
  public static final RendererConfiguration DEFAULT =
      new RendererConfiguration(/* tunneling= */ false);

  /** Whether to enable tunneling. */
  public final boolean tunneling;

  /**
   * @param tunneling Whether to enable tunneling.
   */
  public RendererConfiguration(boolean tunneling) {
    this.tunneling = tunneling;
  }

  @Override
  public boolean equals(@Nullable Object obj) {
    if (this == obj) {
      return true;
    }
    if (obj == null || getClass() != obj.getClass()) {
      return false;
    }
    RendererConfiguration other = (RendererConfiguration) obj;
    return tunneling == other.tunneling;
  }

  @Override
  public int hashCode() {
    return tunneling ? 0 : 1;
  }
}
