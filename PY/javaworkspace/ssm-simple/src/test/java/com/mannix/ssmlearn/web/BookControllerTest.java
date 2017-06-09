package com.mannix.ssmlearn.web;

import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;

import com.mannix.ssmlearn.BaseTest;
import com.mannix.ssmlearn.dto.AppointExecution;
import com.mannix.ssmlearn.dto.Result;

public class BookControllerTest extends BaseTest {
	@Autowired
	private BookController bookController;
	@Test
	public void testAppoint() throws Exception {
        long bookId = 1001;
        long studentId = 12345678910L;
        Result<AppointExecution> execution = bookController.appoint(null,null);
        System.out.println(execution);
    }

}
