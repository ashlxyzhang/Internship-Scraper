package com.scraper.s3;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;

import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.Bucket;

@SpringBootTest
@TestPropertySource(locations = "classpath:test-application.properties")
class S3ApplicationTests {

	@Autowired
	private AmazonS3 amazonS3;

	@Test
	void contextLoads() {
		// Check that AmazonS3 bean is not null
		assertNotNull(amazonS3);

		// Test connection by listing buckets
		List<Bucket> buckets = amazonS3.listBuckets();
		System.out.println("Your Amazon S3 buckets are:");
		for (Bucket b : buckets) {
			System.out.println("* " + b.getName());
		}
	}
}
