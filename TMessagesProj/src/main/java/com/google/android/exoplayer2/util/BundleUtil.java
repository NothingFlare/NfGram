/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.util;

import android.os.Bundle;
import android.os.IBinder;
import androidx.annotation.Nullable;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

/** Utilities for {@link Bundle}. */
public final class BundleUtil {

  private static final String TAG = "BundleUtil";

  @Nullable private static Method getIBinderMethod;
  @Nullable private static Method putIBinderMethod;

  /**
   * Gets an {@link IBinder} inside a {@link Bundle} for all Android versions.
   *
   * @param bundle The bundle to get the {@link IBinder}.
   * @param key The key to use while getting the {@link IBinder}.
   * @return The {@link IBinder} that was obtained.
   */
  @Nullable
  public static IBinder getBinder(Bundle bundle, @Nullable String key) {
    if (Util.SDK_INT >= 18) {
      return bundle.getBinder(key);
    } else {
      return getBinderByReflection(bundle, key);
    }
  }

  /**
   * Puts an {@link IBinder} inside a {@link Bundle} for all Android versions.
   *
   * @param bundle The bundle to insert the {@link IBinder}.
   * @param key The key to use while putting the {@link IBinder}.
   * @param binder The {@link IBinder} to put.
   */
  public static void putBinder(Bundle bundle, @Nullable String key, @Nullable IBinder binder) {
    if (Util.SDK_INT >= 18) {
      bundle.putBinder(key, binder);
    } else {
      putBinderByReflection(bundle, key, binder);
    }
  }

  // Method.invoke may take null "key".
  @SuppressWarnings("nullness:argument")
  @Nullable
  private static IBinder getBinderByReflection(Bundle bundle, @Nullable String key) {
    @Nullable Method getIBinder = getIBinderMethod;
    if (getIBinder == null) {
      try {
        getIBinderMethod = Bundle.class.getMethod("getIBinder", String.class);
        getIBinderMethod.setAccessible(true);
      } catch (NoSuchMethodException e) {
        Log.i(TAG, "Failed to retrieve getIBinder method", e);
        return null;
      }
      getIBinder = getIBinderMethod;
    }

    try {
      return (IBinder) getIBinder.invoke(bundle, key);
    } catch (InvocationTargetException | IllegalAccessException | IllegalArgumentException e) {
      Log.i(TAG, "Failed to invoke getIBinder via reflection", e);
      return null;
    }
  }

  // Method.invoke may take null "key" and "binder".
  @SuppressWarnings("nullness:argument")
  private static void putBinderByReflection(
      Bundle bundle, @Nullable String key, @Nullable IBinder binder) {
    @Nullable Method putIBinder = putIBinderMethod;
    if (putIBinder == null) {
      try {
        putIBinderMethod = Bundle.class.getMethod("putIBinder", String.class, IBinder.class);
        putIBinderMethod.setAccessible(true);
      } catch (NoSuchMethodException e) {
        Log.i(TAG, "Failed to retrieve putIBinder method", e);
        return;
      }
      putIBinder = putIBinderMethod;
    }

    try {
      putIBinder.invoke(bundle, key, binder);
    } catch (InvocationTargetException | IllegalAccessException | IllegalArgumentException e) {
      Log.i(TAG, "Failed to invoke putIBinder via reflection", e);
    }
  }

  private BundleUtil() {}
}
