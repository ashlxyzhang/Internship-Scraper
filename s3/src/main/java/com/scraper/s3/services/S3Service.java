package com.scraper.s3.services;

import java.io.File;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.amazonaws.AmazonServiceException;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.Bucket;
import com.amazonaws.services.s3.model.ObjectListing;
import com.amazonaws.services.s3.model.S3Object;

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

    public S3Object getObject(String bucketName, String objectName) {
        S3Object obj = s3Client.getObject(bucketName, objectName);
        return obj;
    }

    public void putObject(String bucketName, String objectName, String filePath) {
        try {
            s3Client.putObject(bucketName, objectName, new File(filePath));
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }

}
