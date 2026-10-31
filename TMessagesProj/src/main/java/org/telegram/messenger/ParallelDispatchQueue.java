/*
 * Copyright (C) 2026 NothingFlare 
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram.messenger;

import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Drop-in replacement for {@link DispatchQueue} (postRunnable / cancelRunnable / setPriority)
 * backed by a real multi-threaded pool instead of one dedicated Thread.
 *
 * Scoped deliberately to ImageLoader's independent, per-item decode work
 * (thumbnail generation, disk-cache decode, image load) — tasks there don't
 * share mutable state and don't depend on execution order between different
 * files, so parallelizing them is safe. NOT a general substitute for
 * DispatchQueue: many of the 29 other call sites in the app rely on strict
 * serial/ordered execution, so this class is intentionally not used there.
 *
 * Uses ScheduledThreadPoolExecutor (rather than a plain pool) because a
 * couple of call sites pass a small millisecond delay to DispatchQueue as a
 * crude priority hint (0ms vs 1ms) — this preserves that ordering hint while
 * still running tasks across multiple threads.
 */
public class ParallelDispatchQueue {

    private final ScheduledThreadPoolExecutor executor;
    private volatile int threadPriority = Thread.NORM_PRIORITY;

    public ParallelDispatchQueue(String threadName) {
        this(threadName, threadCountForDevice());
    }

    public ParallelDispatchQueue(String threadName, int threads) {
        AtomicInteger counter = new AtomicInteger();
        ThreadFactory factory = r -> {
            Thread t = new Thread(r, threadName + "-" + counter.incrementAndGet());
            try {
                t.setPriority(threadPriority);
            } catch (Exception ignore) {
            }
            return t;
        };
        executor = new ScheduledThreadPoolExecutor(threads, factory);
        executor.setKeepAliveTime(60, TimeUnit.SECONDS);
        executor.allowCoreThreadTimeOut(true);
        executor.setRemoveOnCancelPolicy(true);
    }

    private static int threadCountForDevice() {
        int cores = Runtime.getRuntime().availableProcessors();
        // Leave headroom for the UI thread, network, and other DispatchQueues;
        // clamp so very low-end or very high-core devices both get a sane pool.
        return Math.max(2, Math.min(cores - 1, 6));
    }

    public boolean postRunnable(Runnable runnable) {
        try {
            executor.execute(runnable);
            return true;
        } catch (Exception e) {
            FileLog.e(e);
            return false;
        }
    }

    public boolean postRunnable(Runnable runnable, long delay) {
        try {
            if (delay <= 0) {
                executor.execute(runnable);
            } else {
                executor.schedule(runnable, delay, TimeUnit.MILLISECONDS);
            }
            return true;
        } catch (Exception e) {
            FileLog.e(e);
            return false;
        }
    }

    public void cancelRunnable(Runnable runnable) {
        if (runnable == null) {
            return;
        }
        executor.remove(runnable);
    }

    public void setPriority(int priority) {
        threadPriority = priority;
    }
}
