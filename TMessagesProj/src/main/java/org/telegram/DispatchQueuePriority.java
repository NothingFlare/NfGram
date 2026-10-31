/*
 * Copyright (C) Nikolai Kudashov
 * Copyright (C) 2026 NothingFlare (Modifications)
 *
 * Licensed under GNU GPLv3.
 */

package org.telegram;

import org.telegram.messenger.FileLog;

import java.util.Comparator;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.PriorityBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class DispatchQueuePriority {

    // AyuGram/perf: was hardcoded ThreadPoolExecutor(1, 1, ...) — a single thread handling
    // every priority-queued cache decode in the app. This class has exactly one call site
    // (ImageLoader's cacheOutQueue), so widening its pool is scoped and safe.
    private static int poolSize() {
        int cores = Runtime.getRuntime().availableProcessors();
        return Math.max(2, Math.min(cores - 1, 6));
    }

    ThreadPoolExecutor threadPoolExecutor = new ThreadPoolExecutor(poolSize(), poolSize(), 60, TimeUnit.SECONDS, new PriorityBlockingQueue<>(10, new Comparator<Runnable>() {

        @Override
        public int compare(Runnable o1, Runnable o2) {
            int priority1 = 1;
            int priority2 = 1;
            if (o1 instanceof PriorityRunnable) {
                priority1 = ((PriorityRunnable) o1).priority;
            }
            if (o2 instanceof PriorityRunnable) {
                priority2 = ((PriorityRunnable) o2).priority;
            }
            return priority2 - priority1;
        }
    })) {
        @Override
        protected void beforeExecute(Thread t, Runnable r) {
            CountDownLatch latch = pauseLatch;
            if (latch != null) {
                try {
                    latch.await();
                } catch (InterruptedException e) {
                    FileLog.e(e);
                }
            }
        }
    };

    private volatile CountDownLatch pauseLatch;

    public DispatchQueuePriority(String threadName) {

    }

    public static Runnable wrap(Runnable runnable, int priority) {
        if (priority == 1) {
            return runnable;
        } else {
            return new PriorityRunnable(priority, runnable);
        }
    }

    public void postRunnable(Runnable runnable) {
        threadPoolExecutor.execute(runnable);
    }

    public Runnable postRunnable(Runnable runnable, int priority) {
        if (priority != 1) {
            runnable = new PriorityRunnable(priority, runnable);
        }
        postRunnable(runnable);
        return runnable;
    }

    public void cancelRunnable(Runnable runnable) {
        if (runnable == null) {
            return;
        }
        threadPoolExecutor.remove(runnable);
    }

    public void pause() {
        if (pauseLatch == null) {
            pauseLatch = new CountDownLatch(1);
        }
    }

    public void resume() {
        CountDownLatch latch = pauseLatch;
        if (latch != null) {
            latch.countDown();
            pauseLatch = null;
        }
    }

    private static class PriorityRunnable implements Runnable {
        final int priority;
        final Runnable runnable;

        private PriorityRunnable(int priority, Runnable runnable) {
            this.priority = priority;
            this.runnable = runnable;
        }

        @Override
        public void run() {
            runnable.run();
        }
    }
}
