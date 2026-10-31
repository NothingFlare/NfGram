/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.util;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import javax.annotation.Nonnull;
import javax.annotation.meta.TypeQualifierDefault;
import javax.annotation.meta.When;

/**
 * Annotation for specifying unknown nullness. Useful for clearing the effects of an automatically
 * propagated {@link Nonnull} annotation.
 */
@Nonnull(when = When.UNKNOWN)
@TypeQualifierDefault(ElementType.TYPE_USE)
@Retention(RetentionPolicy.CLASS)
public @interface UnknownNull {}
