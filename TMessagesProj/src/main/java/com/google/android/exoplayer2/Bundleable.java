/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2;

import android.os.Bundle;

/**
 * Interface for classes whose instance can be stored in a {@link Bundle} by {@link #toBundle()} and
 * can be restored from the {@link Bundle} by using the static {@code CREATOR} field that implements
 * {@link Bundleable.Creator}.
 *
 * <p>For example, a {@link Bundleable} class {@code Foo} supports the following:
 *
 * <pre>{@code
 * Foo foo = ...;
 * Bundle fooBundle = foo.toBundle();
 * Foo restoredFoo = Foo.CREATOR.fromBundle(fooBundle);
 * assertThat(restoredFoo).isEqualTo(foo);
 * }</pre>
 */
public interface Bundleable {

  /** Returns a {@link Bundle} representing the information stored in this object. */
  Bundle toBundle();

  /** Interface for the static {@code CREATOR} field of {@link Bundleable} classes. */
  interface Creator<T extends Bundleable> {

    /**
     * Restores a {@link Bundleable} instance from a {@link Bundle} produced by {@link
     * Bundleable#toBundle()}.
     *
     * <p>It guarantees the compatibility of {@link Bundle} representations produced by different
     * versions of {@link Bundleable#toBundle()} by providing best default values for missing
     * fields. It throws an exception if any essential fields are missing.
     */
    T fromBundle(Bundle bundle);
  }
}
