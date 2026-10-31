/*
 * Copyright (C) Radolyn
 *
 * Licensed under GNU GPLv3.
 */

package com.radolyn.ayugram.proprietary;

import com.radolyn.ayugram.database.entities.AyuMessageBase;
import com.radolyn.ayugram.database.entities.EditedMessage;
import com.radolyn.ayugram.messages.AyuSavePreferences;
import org.telegram.messenger.MessageObject;
import org.telegram.messenger.MessagesController;
import org.telegram.tgnet.TLRPC;

public class AyuMessageUtils {

    public static void map(AyuSavePreferences prefs, AyuMessageBase entity) {
        if (prefs == null || entity == null) {
            return;
        }
        entity.userId = prefs.getUserId();
        entity.dialogId = prefs.getDialogId();
        entity.topicId = prefs.getTopicId();
        entity.messageId = prefs.getMessageId();
        entity.entityCreateDate = prefs.getRequestCatchTime();

        TLRPC.Message msg = prefs.getMessage();
        if (msg != null) {
            entity.groupedId = msg.grouped_id;
            entity.peerId = MessageObject.getPeerId(msg.peer_id);
            entity.fromId = MessageObject.getPeerId(msg.from_id);
            entity.date = msg.date;
            entity.flags = msg.flags;
            entity.editDate = msg.edit_date;
            entity.views = msg.views;
            entity.text = msg.message;
            if (msg.fwd_from != null) {
                entity.fwdFromId = MessageObject.getPeerId(msg.fwd_from.from_id);
                entity.fwdName = msg.fwd_from.from_name;
                entity.fwdDate = msg.fwd_from.date;
                entity.fwdPostAuthor = msg.fwd_from.post_author;
            }
            if (msg.reply_to != null) {
                entity.replyMessageId = msg.reply_to.reply_to_msg_id;
                entity.replyTopId = msg.reply_to.reply_to_top_id;
            }
        }
    }

    public static void mapMedia(AyuSavePreferences prefs, AyuMessageBase entity, boolean copyMedia) {
    }

    public static void map(EditedMessage editedMessage, TLRPC.TL_message msg, int currentAccount) {
        if (editedMessage == null || msg == null) {
            return;
        }
        msg.id = editedMessage.messageId;
        msg.dialog_id = editedMessage.dialogId;
        msg.message = editedMessage.text;
        msg.date = editedMessage.entityCreateDate;
        msg.peer_id = MessagesController.getInstance(currentAccount).getPeer(editedMessage.peerId);
        msg.from_id = MessagesController.getInstance(currentAccount).getPeer(editedMessage.fromId);
    }

    public static void mapMedia(EditedMessage editedMessage, TLRPC.TL_message msg) {
    }
}
