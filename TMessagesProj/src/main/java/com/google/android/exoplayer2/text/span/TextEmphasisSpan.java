/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.text.span;

import static java.lang.annotation.ElementType.TYPE_USE;
import static java.lang.annotation.RetentionPolicy.SOURCE;

import androidx.annotation.IntDef;
import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

/**
 * A styling span for text emphasis marks.
 *
 * <p>These are pronunciation aids such as <a
 * href="https://www.w3.org/TR/jlreq/?lang=en#term.emphasis-dots">Japanese boutens</a> which can be
 * rendered using the <a href="https://developer.mozilla.org/en-US/docs/Web/CSS/text-emphasis">
 * text-emphasis</a> CSS property.
 */
// NOTE: There's no Android layout support for text emphasis, so this span currently doesn't extend
// any styling superclasses (e.g. MetricAffectingSpan). The only way to render this emphasis is to
// extract the spans and do the layout manually.
public final class TextEmphasisSpan implements LanguageFeatureSpan {

  /**
   * The possible mark shapes that can be used.
   *
   * <p>One of:
   *
   * <ul>
   *   <li>{@link #MARK_SHAPE_NONE}
   *   <li>{@link #MARK_SHAPE_CIRCLE}
   *   <li>{@link #MARK_SHAPE_DOT}
   *   <li>{@link #MARK_SHAPE_SESAME}
   * </ul>
   */
  @Documented
  @Retention(SOURCE)
  @Target(TYPE_USE)
  @IntDef({MARK_SHAPE_NONE, MARK_SHAPE_CIRCLE, MARK_SHAPE_DOT, MARK_SHAPE_SESAME})
  public @interface MarkShape {}

  public static final int MARK_SHAPE_NONE = 0;
  public static final int MARK_SHAPE_CIRCLE = 1;
  public static final int MARK_SHAPE_DOT = 2;
  public static final int MARK_SHAPE_SESAME = 3;

  /**
   * The possible mark fills that can be used.
   *
   * <p>One of:
   *
   * <ul>
   *   <li>{@link #MARK_FILL_UNKNOWN}
   *   <li>{@link #MARK_FILL_FILLED}
   *   <li>{@link #MARK_FILL_OPEN}
   * </ul>
   */
  @Documented
  @Retention(SOURCE)
  @Target(TYPE_USE)
  @IntDef({MARK_FILL_UNKNOWN, MARK_FILL_FILLED, MARK_FILL_OPEN})
  public @interface MarkFill {}

  public static final int MARK_FILL_UNKNOWN = 0;
  public static final int MARK_FILL_FILLED = 1;
  public static final int MARK_FILL_OPEN = 2;

  /** The mark shape used for text emphasis. */
  public @MarkShape int markShape;

  /** The mark fill for the text emphasis mark. */
  public @MarkShape int markFill;

  /** The position of the text emphasis relative to the base text. */
  public final @TextAnnotation.Position int position;

  public TextEmphasisSpan(
      @MarkShape int shape, @MarkFill int fill, @TextAnnotation.Position int position) {
    this.markShape = shape;
    this.markFill = fill;
    this.position = position;
  }
}
