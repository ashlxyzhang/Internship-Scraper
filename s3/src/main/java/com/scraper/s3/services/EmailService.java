package com.scraper.s3.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

import jakarta.mail.MessagingException;
import jakarta.mail.internet.InternetAddress;
import jakarta.mail.internet.MimeMessage;

import java.util.HashMap;
import java.util.ArrayList;

@Service
public class EmailService {

    @Autowired
    private JavaMailSender sender;

    public void sendEmail(String to, String subject, HashMap<String, ArrayList<ArrayList<String>>> text)
            throws MessagingException {
        MimeMessage msg = sender.createMimeMessage();
        msg.setRecipient(MimeMessage.RecipientType.TO, new InternetAddress(to));
        msg.setSubject(subject);
        msg.setFrom(new InternetAddress("ashleyoftexas@gmail.com"));

        String html = "";
        for (String key : text.keySet()) {
            ArrayList<ArrayList<String>> val = text.get(key);

            if (val.size() != 0) {
                html += String.format("<h2>%s</h2><ul>", key);

                for (int i = 0; i < val.size(); i++) {
                    String internship = val.get(i).get(0);
                    String link = val.get(i).get(1);
                    html += String.format("<li><a href='%s'>%s</a></li>", link, internship);
                }

                html += "</ul>";
            }
        }

        msg.setContent(html, "text/html; charset=utf-8");

        sender.send(msg);
    }
}
