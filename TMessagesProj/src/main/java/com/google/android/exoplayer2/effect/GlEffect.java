/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.effect;

import android.content.Context;
import com.google.android.exoplayer2.util.Effect;
import com.google.android.exoplayer2.util.FrameProcessingException;

/**
 * Interface for a video frame effect with a {@link GlTextureProcessor} implementation.
 *
 * <p>Implementations contain information specifying the effect and can be {@linkplain
 * #toGlTextureProcessor(Context, boolean) converted} to a {@link GlTextureProcessor} which applies
 * the effect.
 */
public interface GlEffect extends Effect {

  /**
   * Returns a {@link SingleFrameGlTextureProcessor} that applies the effect.
   *
   * @param context A {@link Context}.
   * @param useHdr Whether input textures come from an HDR source. If {@code true}, colors will be
   *     in linear RGB BT.2020. If {@code false}, colors will be in linear RGB BT.709.
   */
  GlTextureProcessor toGlTextureProcessor(Context context, boolean useHdr)
      throws FrameProcessingException;
}
