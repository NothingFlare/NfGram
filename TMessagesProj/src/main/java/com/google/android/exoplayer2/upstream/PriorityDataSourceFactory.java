/*
 * Copyright (C) The Android Open Source Project
 *
 * Licensed under GNU GPLv3.
 */

package com.google.android.exoplayer2.upstream;

import com.google.android.exoplayer2.upstream.DataSource.Factory;
import com.google.android.exoplayer2.util.PriorityTaskManager;

/**
 * @deprecated Use {@link PriorityDataSource.Factory}.
 */
@Deprecated
public final class PriorityDataSourceFactory implements Factory {

  private final Factory upstreamFactory;
  private final PriorityTaskManager priorityTaskManager;
  private final int priority;

  /**
   * @param upstreamFactory A {@link DataSource.Factory} to be used to create an upstream {@link
   *     DataSource} for {@link PriorityDataSource}.
   * @param priorityTaskManager The priority manager to which PriorityDataSource task is registered.
   * @param priority The priority of PriorityDataSource task.
   */
  public PriorityDataSourceFactory(
      Factory upstreamFactory, PriorityTaskManager priorityTaskManager, int priority) {
    this.upstreamFactory = upstreamFactory;
    this.priorityTaskManager = priorityTaskManager;
    this.priority = priority;
  }

  @Override
  public PriorityDataSource createDataSource() {
    return new PriorityDataSource(
        upstreamFactory.createDataSource(), priorityTaskManager, priority);
  }
}
