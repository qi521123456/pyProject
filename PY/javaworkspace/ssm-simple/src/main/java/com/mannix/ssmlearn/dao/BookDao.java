package com.mannix.ssmlearn.dao;

import java.util.List;

import org.apache.ibatis.annotations.Param;

import com.mannix.ssmlearn.entity.Book;

public interface BookDao {
	Book queryById(long id);
	/**
     * 查询所有图书
     * 
     * @param offset 查询起始位置
     * @param limit 查询条数
     * @return
     */
	List<Book> queryAll(@Param("offset") int offset, @Param("limit") int limit);
	int reduceNumber(long bookId);
}
