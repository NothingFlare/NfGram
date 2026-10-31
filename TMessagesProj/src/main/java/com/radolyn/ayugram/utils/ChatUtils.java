/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.utils;

import org.telegram.messenger.MessageObject;

public class ChatUtils {

    public static String getMessageText(MessageObject message, Object group) {
        if (message == null) {
            return "";
        }
        if (message.messageOwner != null && message.messageOwner.message != null) {
            return message.messageOwner.message;
        }
        if (message.caption != null) {
            return message.caption.toString();
        }
        return "";
    }

    public static String getMessageText(MessageObject message) {
        return getMessageText(message, null);
    }
}