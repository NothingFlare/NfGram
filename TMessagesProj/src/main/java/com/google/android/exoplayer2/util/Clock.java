/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.util;

import android.os.Handler;
import android.os.Looper;
import androidx.annotation.Nullable;

/**
 * An interface through which system clocks can be read and {@link HandlerWrapper}s created. The
 * {@link #DEFAULT} implementation must be used for all non-test cases.
 */
public interface Clock {

  /** Default {@link Clock} to use for all non-test cases. */
  Clock DEFAULT = new SystemClock();

  /**
   * Returns the current time in milliseconds since the Unix Epoch.
   *
   * @see System#currentTimeMillis()
   */
  long currentTimeMillis();

  /**
   * @see android.os.SystemClock#elapsedRealtime()
   */
  long elapsedRealtime();

  /**
   * @see android.os.SystemClock#uptimeMillis()
   */
  long uptimeMillis();

  /**
   * Creates a {@link HandlerWrapper} using a specified looper and a specified callback for handling
   * messages.
   *
   * @see Handler#Handler(Looper, Handler.Callback)
   */
  HandlerWrapper createHandler(Looper looper, @Nullable Handler.Callback callback);

  /**
   * Notifies the clock that the current thread is about to be blocked and won't return until a
   * condition on another thread becomes true.
   *
   * <p>Should be a no-op for all non-test cases.
   */
  void onThreadBlocked();
}
