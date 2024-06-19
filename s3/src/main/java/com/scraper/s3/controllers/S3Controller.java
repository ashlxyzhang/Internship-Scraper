package com.scraper.s3.controllers;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.s3.model.ObjectListing;
import com.amazonaws.services.s3.model.S3Object;
import com.scraper.s3.services.S3Service;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

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
    public S3Object getObject(@PathVariable String bucketName, @PathVariable String objectName) {
        return s3Service.getObject(bucketName, objectName);
    }

    @PostMapping("/putObject/{bucketName}/{objectName}/{filePath}")
    public void putObject(@PathVariable String bucketName, @PathVariable String objectName,
            @PathVariable String filePath) {
        s3Service.putObject(bucketName, objectName, filePath);
    }

}
