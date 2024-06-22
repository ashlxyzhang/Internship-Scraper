package com.scraper.s3.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.scraper.s3.services.EmailService;

import jakarta.mail.MessagingException;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.HashMap;
import java.util.ArrayList;

@RestController
@RequestMapping("/api/email")
public class EmailController {

    @Autowired
    private EmailService emailService;

    @GetMapping("/send/{to}/{subject}")
    public void sendEmail(@PathVariable String to, @PathVariable String subject, @RequestParam String text) {
        ObjectMapper objectMapper = new ObjectMapper();
        HashMap<String, ArrayList<ArrayList<String>>> textMap;
        try {
            textMap = objectMapper.readValue(text, new TypeReference<HashMap<String, ArrayList<ArrayList<String>>>>() {
            });
        } catch (Exception e) {
            throw new RuntimeException("Failed to parse JSON", e);
        }
        try {
            emailService.sendEmail(to, subject, textMap);
        } catch (MessagingException e) {
            e.printStackTrace();
        }
    }

}
