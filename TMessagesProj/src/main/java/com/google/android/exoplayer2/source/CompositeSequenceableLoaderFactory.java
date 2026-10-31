/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source;

/** A factory to create composite {@link SequenceableLoader}s. */
public interface CompositeSequenceableLoaderFactory {

  /**
   * Creates a composite {@link SequenceableLoader}.
   *
   * @param loaders The sub-loaders that make up the {@link SequenceableLoader} to be built.
   * @return A composite {@link SequenceableLoader} that comprises the given loaders.
   */
  SequenceableLoader createCompositeSequenceableLoader(SequenceableLoader... loaders);
}
