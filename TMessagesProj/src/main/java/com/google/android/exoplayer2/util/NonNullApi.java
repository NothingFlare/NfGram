/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.util;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

/**
 * Annotation to declare all type usages in the annotated instance as {@link Nonnull}, unless
 * explicitly marked with a nullable annotation.
 */
@Retention(RetentionPolicy.CLASS)
public @interface NonNullApi {}
