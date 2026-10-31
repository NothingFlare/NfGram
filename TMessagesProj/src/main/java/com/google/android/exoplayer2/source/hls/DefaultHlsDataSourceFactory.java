/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.source.hls;

import com.google.android.exoplayer2.C;
import com.google.android.exoplayer2.upstream.DataSource;

/** Default implementation of {@link HlsDataSourceFactory}. */
public final class DefaultHlsDataSourceFactory implements HlsDataSourceFactory {

  private final DataSource.Factory dataSourceFactory;

  /**
   * @param dataSourceFactory The {@link DataSource.Factory} to use for all data types.
   */
  public DefaultHlsDataSourceFactory(DataSource.Factory dataSourceFactory) {
    this.dataSourceFactory = dataSourceFactory;
  }

  @Override
  public DataSource createDataSource(@C.DataType int dataType) {
    return dataSourceFactory.createDataSource();
  }
}
