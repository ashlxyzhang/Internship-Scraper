package com.scraper.s3.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.amazonaws.auth.AWSCredentials;
import com.amazonaws.auth.AWSStaticCredentialsProvider;
import com.amazonaws.auth.BasicAWSCredentials;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;

import jakarta.annotation.PostConstruct;

@Configuration
public class BucketConfig {

    @Value("${aws.access.key}")
    private String awsAccessKey;

    @Value("${aws.secret.key}")
    private String awsSecretKey;

    @PostConstruct
    public void init() {
        System.out.println("AWS Access Key: " + awsAccessKey);
        System.out.println("AWS Secret Key: " + awsSecretKey);
    }

    @Bean
    public AmazonS3 getS3Client() {
        AWSCredentials creds = new BasicAWSCredentials(awsAccessKey, awsSecretKey);
        return AmazonS3ClientBuilder.standard()
                .withCredentials(new AWSStaticCredentialsProvider(creds))
                .withRegion(Regions.US_EAST_1)
                .build();
    }
}
