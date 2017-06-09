package com.mannix.ssmlearn.service.impl;

import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;

import com.mannix.ssmlearn.BaseTest;
import com.mannix.ssmlearn.dto.AppointExecution;
import com.mannix.ssmlearn.service.BookService;

public class BookServiceImplTest extends BaseTest {
	@Autowired
    private BookService bookService;

    @Test
    public void testAppoint() throws Exception {
        long bookId = 1001;
        long studentId = 12345678910L;
        AppointExecution execution = bookService.appoint(bookId, studentId);
        System.out.println(execution);
    }
}
