package com.mannix.ssmlearn.dao;

import java.util.List;

import org.apache.ibatis.annotations.Param;

import com.mannix.ssmlearn.entity.Book;

public interface BookDao {
	Book queryById(long id);
	/**
     * ��ѯ����ͼ��
     * 
     * @param offset ��ѯ��ʼλ��
     * @param limit ��ѯ����
     * @return
     */
	List<Book> queryAll(@Param("offset") int offset, @Param("limit") int limit);
	int reduceNumber(long bookId);
}
