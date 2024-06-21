package com.scraper.s3.controllers;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.s3.model.ObjectListing;
import com.amazonaws.services.s3.model.S3Object;
import com.scraper.s3.services.S3Service;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

import java.io.IOException;
import java.io.File;

@RestController
@RequestMapping("/api/s3")
public class S3Controller {

    @Autowired
    private S3Service s3Service;

    @GetMapping("/buckets")
    public List<Bucket> getBuckets() {
        return s3Service.getBuckets();
    }

    @GetMapping("/validate/{bucketName}")
    public boolean validateBucket(@PathVariable String bucketName) {
        return s3Service.validateBucket(bucketName);
    }

    @GetMapping("/objects/{bucketName}")
    public ObjectListing getObjects(@PathVariable String bucketName) {
        return s3Service.getObjects(bucketName);
    }

    @GetMapping("/object/{bucketName}/{objectName}")
    public String getObject(@PathVariable String bucketName, @PathVariable String objectName) {
        return s3Service.getObject(bucketName, objectName);
    }

    @PostMapping("/putObject/{bucketName}/{objectName}")
    public void putObject(@PathVariable String bucketName, @PathVariable String objectName,
            @RequestParam MultipartFile file) throws IOException {
        try {
            File temp = File.createTempFile("temp", null);
            file.transferTo(temp);

            s3Service.putObject(bucketName, objectName, temp);

            temp.delete();
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

}
