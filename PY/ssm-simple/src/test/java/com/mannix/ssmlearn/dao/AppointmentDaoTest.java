package com.mannix.ssmlearn.dao;

import org.junit.Test;
import org.springframework.beans.factory.annotation.Autowired;

import com.mannix.ssmlearn.BaseTest;
import com.mannix.ssmlearn.entity.Appointment;

public class AppointmentDaoTest extends BaseTest {
	@Autowired
    private AppointmentDao appointmentDao;

//	@Test
//    public void testInsertAppointment() throws Exception {
//        long bookId = 1000;
//        long studentId = 12345678910L;
//        int insert = appointmentDao.insertAppointment(bookId, studentId);
//        System.out.println("insert=" + insert);
//    }

    @Test
    public void testQueryByKeyWithBook() throws Exception {
        long bookId = 1000;
        long studentId = 12345678910L;
        Appointment appointment = appointmentDao.queryByKeyWithBook(bookId, studentId);
        System.out.println(appointment.toString());
        System.out.println(appointment.getBook());
    }
}
