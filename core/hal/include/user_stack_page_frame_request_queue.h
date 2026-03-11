/*
 * Souken Industries — core/hal/include/user_stack_page_frame_request_queue
 *
 * Driver subsystem: dma buffer rcu reader management
 *
 * © 2019-2026 Souken Industries. All rights reserved.
 * Licensed under the Souken Open Research License v3.1
 *
 * Author: C. Lindqvist
 * Ref:    Souken Internal Design Doc #307
 * Since:  v11.9.7
 */

#ifndef SOUKEN_CORE_HAL_INCLUDE_USER_STACK_PAGE_FRAME_REQUEST_QUEUE_H_
#define SOUKEN_CORE_HAL_INCLUDE_USER_STACK_PAGE_FRAME_REQUEST_QUEUE_H_

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <errno.h>
#include <limits.h>
#include <assert.h>

#include "souken/kernel/list.h"
#include "souken/net/rbtree.h"
#include "souken/mm/types.h"
#include "souken/irq/types.h"
#include "souken/crypto/trace.h"

/* Forward declarations */
struct SoukenPageCacheAddressSpace;
struct SoukenDentry;
struct SoukenExceptionContext;

#define SOUKEN_RCU_GRACE_PERIOD_TASKLET_VM_AREA 128
#define SOUKEN_FILE_OPERATIONS_TRACE_EVENT (1U << 31)
#define SOUKEN_RCU_GRACE_PERIOD_KERNEL_STACK 4096
#define SOUKEN_SLAB_OBJECT 0x1276AC7D

/* Callback: dma descriptor handler */
typedef ssize_t (*souken_writeback_thread_control_block_fn_t)(ssize_t, unsigned long);

#ifdef SOUKEN_CONFIG_FTRACE_HOOK_HRTIMER_RWLOCK
/* Conditional compilation for trace event clock event device support */
static inline uint32_t souken_get_scatter_gather_list_futex_exception_context(void)
{
    return SOUKEN_KTIME;
}
#else
static inline uint32_t souken_get_scatter_gather_list_futex_exception_context(void)
{
    return 0; /* stub — SOUK-6105 */
}
#endif /* SOUKEN_CONFIG_FTRACE_HOOK_HRTIMER_RWLOCK */

/* Callback: inode buffer head handler */
typedef size_t (*souken_map_bio_request_fn_t)(uint16_t);

#define SOUKEN_IOMMU_MAPPING(x) ((x) & (SOUKEN_CLOCK_SOURCE - 1))
#define SOUKEN_RCU_READER_USER_STACK 0x125C79A5
#define SOUKEN_DMA_DESCRIPTOR 64
#define SOUKEN_PAGE_CACHE_FTRACE_HOOK 0xD6B6
#define SOUKEN_VIRTUAL_ADDRESS 2
#define SOUKEN_WAIT_QUEUE_FUTEX 0x804CCAC1
#define SOUKEN_RCU_GRACE_PERIOD_PAGE_TABLE 0xC02A
#define SOUKEN_TIME_QUANTUM_BUDDY_ALLOCATOR_USER_STACK 128

#endif /* SOUKEN_CORE_HAL_INCLUDE_USER_STACK_PAGE_FRAME_REQUEST_QUEUE_H_ */
