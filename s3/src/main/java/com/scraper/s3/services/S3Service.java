package com.scraper.s3.services;

import java.io.File;
import java.io.IOException;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.s3.model.ObjectListing;
import com.amazonaws.services.s3.model.PutObjectRequest;
import com.amazonaws.services.s3.model.S3Object;

import java.io.BufferedReader;
import java.io.InputStreamReader;

@Service
public class S3Service {

    @Autowired
    private AmazonS3 s3Client;

    public List<Bucket> getBuckets() {
        return s3Client.listBuckets();
    }

    public boolean validateBucket(String name) {
        List<Bucket> buckets = getBuckets();
        return buckets.stream().anyMatch(m -> name.equals(m.getName()));
    }

    public ObjectListing getObjects(String bucketName) {
        ObjectListing objs = s3Client.listObjects(bucketName);
        return objs;
    }

    public String getObject(String bucketName, String objectName) {
        S3Object obj = s3Client.getObject(bucketName, objectName);
        BufferedReader reader = new BufferedReader(new InputStreamReader(obj.getObjectContent()));
        try {
            String line = reader.readLine();
            String result = "";
            while (line != null) {
                result += line + "\n";
                line = reader.readLine();
            }
            return result;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void putObject(String bucketName, String objectName, File file) {
        try {
            PutObjectRequest por = new PutObjectRequest(bucketName, objectName, file);
            s3Client.putObject(por);
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
