/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.util;

/**
 * Represents an operation that accepts a single input argument and returns no result. Unlike most
 * other functional interfaces, Consumer is expected to operate via side-effects.
 */
public interface Consumer<T> {

  /** Performs this operation on the given argument. */
  void accept(T t);
}
