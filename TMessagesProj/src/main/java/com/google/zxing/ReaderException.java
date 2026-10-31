/*
 * Copyright (C) ZXing authors
 *
 * Licensed under GNU GPLv3.
 */

package com.google.zxing;

/**
 * The general exception class throw when something goes wrong during decoding of a barcode.
 * This includes, but is not limited to, failing checksums / error correction algorithms, being
 * unable to locate finder timing patterns, and so on.
 *
 * @author Sean Owen
 */
public abstract class ReaderException extends Exception {

  // disable stack traces when not running inside test units
  protected static final boolean isStackTrace =
      System.getProperty("surefire.test.class.path") != null;
  protected static final StackTraceElement[] NO_TRACE = new StackTraceElement[0];

  ReaderException() {
    // do nothing
  }

  ReaderException(Throwable cause) {
    super(cause);
  }

  // Prevent stack traces from being taken
  @Override
  public final synchronized Throwable fillInStackTrace() {
    return null;
  }

}
