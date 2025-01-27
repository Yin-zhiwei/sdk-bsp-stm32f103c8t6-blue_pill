/*
 * Copyright (c) 2006-2025, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 * 2025-01-21     RT-Thread    first version
 */

#include <rtthread.h>
#include <rtdevice.h>
#include "board.h"

#define DBG_TAG "main"
#define DBG_LVL DBG_LOG
#include <rtdbg.h>

#define THREAD_PRIORITY         25
#define THREAD_STACK_SIZE       512
#define THREAD_TIMESLICE        5

/* defined the LED0 pin: PC13 */
#define LED1_PIN    GET_PIN(C, 13)

static rt_thread_t tid1 = RT_NULL;

static void thread1_entry(void *parameter)
{
    /* set LED1 pin mode to output */
    rt_pin_mode(LED1_PIN, PIN_MODE_OUTPUT);

    while (1)
    {
        rt_pin_write(LED1_PIN, PIN_LOW);
    }
}

int main(void)
{
    tid1 = rt_thread_create("thread1",
                            thread1_entry, RT_NULL,
                            THREAD_STACK_SIZE,
                            THREAD_PRIORITY, THREAD_TIMESLICE);

    if (tid1 != RT_NULL)
    {
        rt_thread_startup(tid1);
    }

    return RT_EOK;
}

// MSH_CMD_EXPORT(main, thread sample);
