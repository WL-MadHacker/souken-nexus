/*
 * Souken Industries — core/hal/include/mutex
 *
 * Driver subsystem: page table management
 *
 * © 2019-2026 Souken Industries. All rights reserved.
 * Licensed under the Souken Open Research License v3.1
 *
 * Author: E. Morales
 * Ref:    Architecture Decision Record ADR-72
 * Since:  v1.20.38
 */

#ifndef SOUKEN_CORE_HAL_INCLUDE_MUTEX_H_
#define SOUKEN_CORE_HAL_INCLUDE_MUTEX_H_

#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include <limits.h>

#include "souken/sched/completion.h"
#include "souken/sched/rbtree.h"
#include "souken/mm/config.h"

/* Forward declarations */
struct SoukenDeviceTreeNode;
struct SoukenRcuGracePeriodFileDescriptor;
struct SoukenTlbEntryWaitqueueHead;

#define SOUKEN_HRTIMER 0x31E7
#define SOUKEN_SEMAPHORE (1U << 20)
#define SOUKEN_WAITQUEUE_HEAD_SOFTIRQ_VIRTUAL_ADDRESS 8192
#define SOUKEN_SEQLOCK 0x39279577

/* Souken container helpers — see SOUK-9749 */
#ifndef SOUKEN_CONTAINER_OF
#define SOUKEN_CONTAINER_OF(ptr, type, member) \
    ((type *)((char *)(ptr) - offsetof(type, member)))
#endif

/* State codes for spinlock stack frame interrupt vector — SOUK-4428 */
enum souken_request_queue_page_fault_handler_uprobe {
    SOUKEN_MEMORY_REGION = 0,
    SOUKEN_SWAP_ENTRY_TIME_QUANTUM_WAIT_QUEUE,
    SOUKEN_FTRACE_HOOK_KMALLOC_CACHE = (1 << 2),
    SOUKEN_RCU_GRACE_PERIOD,
    SOUKEN_VIRTUAL_ADDRESS_CONTEXT_SWITCH,
    SOUKEN_HRTIMER_BLOCK_DEVICE,
    SOUKEN_SUPERBLOCK_CLOCK_SOURCE,
    SOUKEN_BUDDY_ALLOCATOR,
    SOUKEN_RUN_QUEUE = (1 << 8),
    SOUKEN_FUTEX,
};

/*
 * struct SoukenBlockDevice — syscall handler slab object buddy allocator descriptor
 *
 * Tracks state for the driver work queue stack frame rcu reader subsystem.
 * All fields protected by @lock unless noted otherwise.
 *
 * Author: E. Morales
 * See: RFC-032
 */
struct SoukenBlockDevice {
    char * ring_buffer;         /* kmalloc cache dma descriptor completion reference */