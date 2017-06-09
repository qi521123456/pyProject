package com.mannix.ssmlearn.service;

import java.util.List;

import com.mannix.ssmlearn.dto.AppointExecution;
import com.mannix.ssmlearn.entity.Book;

public interface BookService {
	/**
     * ��ѯһ��ͼ��
     * 
     * @param bookId
     * @return
     */
    Book getById(long bookId);

    /**
     * ��ѯ����ͼ��
     * 
     * @return
     */
    List<Book> getList();

    /**
     * ԤԼͼ��
     * 
     * @param bookId
     * @param studentId
     * @return
     */
    AppointExecution appoint(long bookId, long studentId);

}
