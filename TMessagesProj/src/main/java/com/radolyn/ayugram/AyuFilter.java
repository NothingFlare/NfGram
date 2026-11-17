/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram;

import android.text.TextUtils;
import android.util.LongSparseArray;
import com.radolyn.ayugram.utils.ChatUtils;
import org.telegram.messenger.FileLog;
import org.telegram.messenger.MessageObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.regex.Pattern;

public class AyuFilter {
    private static final Object sync = new Object();
    private static ArrayList<Pattern> patterns;
    private static LongSparseArray<HashMap<Integer, Boolean>> filteredCache;
    private static final int MAX_CACHED_DIALOGS = 50;

    public static void rebuildCache() {
        synchronized (sync) {
            var filters = AyuConfig.getRegexFilters();

            var flags = Pattern.MULTILINE;
            if (AyuConfig.regexFiltersCaseInsensitive) {
                flags |= Pattern.CASE_INSENSITIVE;
            }

            patterns = new ArrayList<>();
            for (var filter : filters) {
                if (TextUtils.isEmpty(filter)) {
                    continue;
                }
                try {
                    patterns.add(Pattern.compile(filter, flags));
                } catch (Throwable t) {
                    FileLog.e("AyuFilter: invalid regex pattern: " + filter, t);
                }
            }

            filteredCache = new LongSparseArray<>();
        }
    }

    private static boolean isFiltered(CharSequence text) {
        if (!AyuConfig.regexFiltersEnabled) {
            return false;
        }

        if (TextUtils.isEmpty(text)) {
            return false;
        }

        ArrayList<Pattern> localPatterns;
        synchronized (sync) {
            if (patterns == null) {
                return false;
            }
            localPatterns = patterns;
        }

        for (var pattern : localPatterns) {
            try {
                if (pattern.matcher(text).find()) {
                    return true;
                }
            } catch (Throwable t) {
                FileLog.e(t);
            }
        }

        return false;
    }

    public static boolean isFiltered(MessageObject msg, MessageObject.GroupedMessages group) {
        if (!AyuConfig.regexFiltersEnabled) {
            return false;
        }

        if (msg == null) {
            return false;
        }

        synchronized (sync) {
            if (patterns == null || filteredCache == null) {
                rebuildCache();
            }

            var cached = filteredCache.get(msg.getDialogId());
            if (cached != null) {
                Boolean res = cached.get(msg.getId());
                if (res != null) {
                    return res;
                }
            }

            boolean res = isFiltered(ChatUtils.getMessageText(msg, group));

            if (filteredCache.size() > MAX_CACHED_DIALOGS) {
                filteredCache.clear();
                cached = null;
            }

            if (cached == null) {
                cached = new HashMap<>();
                filteredCache.put(msg.getDialogId(), cached);
            }

            cached.put(msg.getId(), res);

            if (group != null && group.messages != null && !group.messages.isEmpty()) {
                for (var m : group.messages) {
                    if (m != null) {
                        cached.put(m.getId(), res);
                    }
                }
            }

            return res;
        }
    }
}
