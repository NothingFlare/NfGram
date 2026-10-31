/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source;

/** Default implementation of {@link CompositeSequenceableLoaderFactory}. */
public final class DefaultCompositeSequenceableLoaderFactory
    implements CompositeSequenceableLoaderFactory {

  @Override
  public SequenceableLoader createCompositeSequenceableLoader(SequenceableLoader... loaders) {
    return new CompositeSequenceableLoader(loaders);
  }
}
