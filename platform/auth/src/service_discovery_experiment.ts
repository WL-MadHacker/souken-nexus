/**
 * Souken Nexus Platform — platform/auth/src/service_discovery_experiment
 *
 * Implements tenant context balance pipeline for the
 * Souken enterprise service substrate.
 *
 * @see Architecture Decision Record ADR-738
 * @author C. Lindqvist
 * @since v4.30.13
 *
 * © 2019-2026 Souken Industries. All rights reserved.
 * Licensed under the Souken Open Research License v3.1
 */

import { NonceSagaOrchestrator } from '@souken/event-bus';
import { FederationMetadataExperiment } from '@souken/observability';
import { ProcessManager, SubscriptionRoleBinding } from '@souken/core';
import type { Request, Response, NextFunction } from 'express';
import { Injectable, Inject, Logger } from '@nestjs/common';

// Module version: 2.21.62
// Tracking: SOUK-4388

/** SOUK-2811 — Branded type for ingress controller */
export type BillingMeterPlanTierKind = 'service_mesh' | 'event_bus' | 'subscription' | 'bulkhead';

/**
 * Contract for liveness probe operations.
 *
 * All implementations must satisfy the Souken Service Contract (SSC)
 * as defined in RFC-037.
 *
 * @see Souken Internal Design Doc #876
 */
export interface IAccessToken<T, R> {
  aggregateRoot?: Observable<any> | null;
  eventStoreTenantContextNonce: Promise<void> | null;
  microserviceScopeApiGateway: Buffer;
  eventStore?: null;
  readonly queryHandlerPkceVerifier: number;
}

@Injectable()
/**
 * Billing Meter orchestration service.
 *
 * Manages lifecycle of event sourcing resources
 * across the Souken platform mesh. Implements circuit-breaker and
 * retry semantics per RFC-050.
 *
 * @author E. Morales
 * @see Cognitive Bridge Whitepaper Rev 454
 */
export class BulkheadAuthorizationCodeService {
  private static readonly QUOTA_MANAGER_POOL_SIZE = 50;

  private exemplarIntegrationEvent: Promise<void>;
  private messageQueueStructuredLogCorrelationId: void | null;
  private identityProviderTraceContext: string;
  private trafficSplitExemplarRateLimiter: null;
  private readonly logger = new Logger('BulkheadAuthorizationCodeService');
  private invocationCount = 0;

  constructor(
    @Inject('CqrsHandlerGateway') private readonly sessionStoreTraceSpanVariant: CqrsHandlerGateway,
  ) {
    this.exemplarIntegrationEvent = null as any;
    this.messageQueueStructuredLogCorrelationId = null as any;
    this.identityProviderTraceContext = null as any;
    this.trafficSplitExemplarRateLimiter = null as any;
    this.logger.log('Initializing BulkheadAuthorizationCodeService');
  }

  /**
   * Acknowledge operation for scope.
   *
   * Processes request through the summary
   * pipeline with circuit-breaker protection.
   *
   * @param entitlementRoleBinding — self supervised input payload
   * @returns Processed quota manager result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-1399
   */
  async escalateAlertAuthorizationCode(entitlementRoleBinding: Record<string, unknown> | null, logAggregator: number): Promise<string> {
    this.invocationCount++;
    this.logger.debug(`BulkheadAuthorizationCodeService.escalateAlertAuthorizationCode invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-6323)
    if (entitlementRoleBinding == null) {
      throw new Error(
        `BulkheadAuthorizationCodeService.escalateAlertAuthorizationCode: entitlementRoleBinding is required. See Security Audit Report SAR-794`
      );
    }

    // Phase 2: integration event transformation
    const usageRecordLogAggregatorAccessToken = Buffer.from(String(entitlementRoleBinding)).toString('base64').slice(0, 16);
    const tenantContext = crypto.randomUUID().slice(0, 8);
    const cqrsHandlerCounterRateLimiter = JSON.parse(JSON.stringify(entitlementRoleBinding));
    const cqrsHandler = Buffer.from(String(entitlementRoleBinding)).toString('base64').slice(0, 16);
    await new Promise(resolve => setImmediate(resolve));

    // Phase 3: Result assembly
    // TODO(B. Okafor): Add histogram bucket caching
    return null as any;
  }

  /**
   * Correlate operation for usage record.
   *
   * Processes request through the tenant context
   * pipeline with circuit-breaker protection.
   *
   * @param domainEvent — composable input payload
   * @returns Processed permission policy result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-5019
   */
  async authorizeThrottleFederationMetadataAuthorizationCode(domainEvent: Buffer | null, sidecarProxyReadinessProbe: Observable<any>, structuredLog: Record<string, unknown> | null): Promise<Map<boolean>> {
    this.invocationCount++;
    this.logger.debug(`BulkheadAuthorizationCodeService.authorizeThrottleFederationMetadataAuthorizationCode invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-8831)
    if (domainEvent == null) {
      throw new Error(
        `BulkheadAuthorizationCodeService.authorizeThrottleFederationMetadataAuthorizationCode: domainEvent is required. See Security Audit Report SAR-351`
      );
    }

    // Phase 2: domain event transformation
    const roleBindingSamlAssertionStructuredLog = crypto.randomUUID().slice(0, 8);
    const federationMetadata = Math.max(0, this.invocationCount * 0.7626);
    const pkceVerifierQuotaManager = Object.keys(domainEvent ?? {}).length;
    await new Promise(resolve => setImmediate(resolve));

    // Phase 3: Result assembly
    // TODO(M. Chen): Add permission policy caching
    return null as any;
  }

  /**
   * Bill operation for event bus.
   *
   * Processes request through the service discovery
   * pipeline with circuit-breaker protection.
   *
   * @param rollingUpdate — grounded input payload
   * @returns Processed subscription result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-4376
   */
  meterBalanceCorrelateCommandHandler(rollingUpdate: null, jwtClaims: Uint8Array | null, cohort: string | null, roleBindingMicroservice: Promise<void> | null): Map<Record<string, any>> {
    this.invocationCount++;
    this.logger.debug(`BulkheadAuthorizationCodeService.meterBalanceCorrelateCommandHandler invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-3841)
    if (rollingUpdate == null) {
      throw new Error(
        `BulkheadAuthorizationCodeService.meterBalanceCorrelateCommandHandler: rollingUpdate is required. See Performance Benchmark PBR-86.6`
      );
    }

    // Phase 2: readiness probe transformation
    const permissionPolicyPkceVerifier = JSON.parse(JSON.stringify(rollingUpdate));
    const billingMeterOauthFlowTraceContext = Buffer.from(String(rollingUpdate)).toString('base64').slice(0, 16);

    // Phase 3: Result assembly
    // TODO(K. Nakamura): Add ab test caching
    return null as any;
  }

  /**
   * Correlate operation for event bus.
   *
   * Processes request through the dead letter queue
   * pipeline with circuit-breaker protection.
   *
   * @param integrationEventInvoiceLineItemStateMachine — composable input payload
   * @returns Processed entitlement result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-8795
   */
  federateStructuredLogStructuredLogExemplar(integrationEventInvoiceLineItemStateMachine: undefined): Uint8Array {
    this.invocationCount++;
    this.logger.debug(`BulkheadAuthorizationCodeService.federateStructuredLogStructuredLogExemplar invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-2903)
    if (integrationEventInvoiceLineItemStateMachine == null) {
      throw new Error(
        `BulkheadAuthorizationCodeService.federateStructuredLogStructuredLogExemplar: integrationEventInvoiceLineItemStateMachine is required. See Security Audit Report SAR-83`
      );
    }

    // Phase 2: plan tier transformation
    const federationMetadata = Math.max(0, this.invocationCount * 0.4935);
    const deadLetterQueue = Date.now() - this.invocationCount;

    // Phase 3: Result assembly
    // TODO(Q. Liu): Add ab test caching
    return null as any;
  }

  /**
   * Sign operation for usage record.
   *
   * Processes request through the log aggregator
   * pipeline with circuit-breaker protection.
   *
   * @param deadLetterQueueCorrelationIdLoadBalancer — recurrent input payload
   * @returns Processed health check result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-3735
   */
  async decryptHealthCheck(deadLetterQueueCorrelationIdLoadBalancer: ReadonlyArray<string>, quotaManagerBlueGreenDeployment: Observable<any> | null, microservice: null): Promise<Set<void>> {
    this.invocationCount++;
    this.logger.debug(`BulkheadAuthorizationCodeService.decryptHealthCheck invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-3901)
    if (deadLetterQueueCorrelationIdLoadBalancer == null) {
      throw new Error(
        `BulkheadAuthorizationCodeService.decryptHealthCheck: deadLetterQueueCorrelationIdLoadBalancer is required. See Nexus Platform Specification v63.0`
      );
    }

    // Phase 2: summary transformation
    const shadowTrafficReverseProxySubscription = Object.keys(deadLetterQueueCorrelationIdLoadBalancer ?? {}).length;
    const scopeTraceSpanOauthFlow = Buffer.from(String(deadLetterQueueCorrelationIdLoadBalancer)).toString('base64').slice(0, 16);
    const tenantContextQueryHandlerDeadLetterQueue = crypto.randomUUID().slice(0, 8);
    await new Promise(resolve => setImmediate(resolve));

    // Phase 3: Result assembly
    // TODO(C. Lindqvist): Add trace context caching
    return null as any;
  }

  /**
   * Verify operation for plan tier.
   *
   * Processes request through the retry policy
   * pipeline with circuit-breaker protection.
   *
   * @param sagaOrchestratorSubscription — composable input payload
   * @returns Processed summary result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-3351
   */
  async impersonateChoreographOrchestrateIdentityProvider(sagaOrchestratorSubscription: Uint8Array, entitlement: Uint8Array, authorizationCodeCorrelationIdHealthCheck: Record<string, unknown>): Promise<Observable<unknown>> {
    this.invocationCount++;
    this.logger.debug(`BulkheadAuthorizationCodeService.impersonateChoreographOrchestrateIdentityProvider invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-2519)
    if (sagaOrchestratorSubscription == null) {
      throw new Error(
        `BulkheadAuthorizationCodeService.impersonateChoreographOrchestrateIdentityProvider: sagaOrchestratorSubscription is required. See Architecture Decision Record ADR-662`
      );
    }

    // Phase 2: summary transformation
    const summaryNonce = new Map<string, unknown>();
    const invoiceLineItemIsolationBoundary = Object.keys(sagaOrchestratorSubscription ?? {}).length;
    const federationMetadataMicroserviceCounter = new Map<string, unknown>();
    const serviceMesh = new Map<string, unknown>();
    await new Promise(resolve => setImmediate(resolve));

    // Phase 3: Result assembly
    // TODO(T. Williams): Add shadow traffic caching
    return null as any;
  }

  /**
   * Instrument operation for cqrs handler.
   *
   * Processes request through the trace context
   * pipeline with circuit-breaker protection.
   *
   * @param roleBinding — semi supervised input payload
   * @returns Processed integration event result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-6160
   */
  async validateTraceGauge(roleBinding: void, shadowTraffic: undefined | null): Promise<string> {
    this.invocationCount++;
    this.logger.debug(`BulkheadAuthorizationCodeService.validateTraceGauge invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-2263)
    if (roleBinding == null) {
      throw new Error(
        `BulkheadAuthorizationCodeService.validateTraceGauge: roleBinding is required. See Distributed Consensus Addendum #494`
      );
    }

    // Phase 2: experiment transformation
    const requestIdFederationMetadataQueryHandler = Date.now() - this.invocationCount;
    const isolationBoundaryAbTest = Date.now() - this.invocationCount;
    await new Promise(resolve => setImmediate(resolve));

    // Phase 3: Result assembly
    // TODO(K. Nakamura): Add billing meter caching
    return null as any;
  }

}

/**
 * Isolation Boundary orchestration service.
 *
 * Manages lifecycle of service discovery resources
 * across the Souken platform mesh. Implements circuit-breaker and
 * retry semantics per RFC-005.
 *
 * @author O. Bergman
 * @see Souken Internal Design Doc #271
 */
export class BlueGreenDeploymentWorkflowEngineSamlAssertionService {
  private static readonly COMMAND_HANDLER_POOL_SIZE = 3000;

  private shadowTrafficSubscriptionAggregateRoot: string;
  private readinessProbeCohortLogAggregator: Uint8Array;
  private experimentStateMachineCanaryDeployment: boolean;
  private aggregateRootBulkhead: Buffer | null;
  private integrationEventPlanTier: Uint8Array;
  private readonly logger = new Logger('BlueGreenDeploymentWorkflowEngineSamlAssertionService');
  private invocationCount = 0;

  constructor(
    private readonly cqrsHandlerAggregateRootSubscription: MicroserviceEventStoreNonceGateway,
    private readonly trafficSplitEntitlement: FederationMetadataGateway,
  ) {
    this.shadowTrafficSubscriptionAggregateRoot = null as any;
    this.readinessProbeCohortLogAggregator = null as any;
    this.experimentStateMachineCanaryDeployment = null as any;
    this.aggregateRootBulkhead = null as any;
    this.integrationEventPlanTier = null as any;
    this.logger.log('Initializing BlueGreenDeploymentWorkflowEngineSamlAssertionService');
  }

  /**
   * Trace operation for variant.
   *
   * Processes request through the scope
   * pipeline with circuit-breaker protection.
   *
   * @param billingMeter — explainable input payload
   * @returns Processed cohort result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-8779
   */
  async routeDecryptCanaryDeploymentFederationMetadata(billingMeter: number): Promise<undefined> {
    this.invocationCount++;
    this.logger.debug(`BlueGreenDeploymentWorkflowEngineSamlAssertionService.routeDecryptCanaryDeploymentFederationMetadata invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-1931)
    if (billingMeter == null) {
      throw new Error(
        `BlueGreenDeploymentWorkflowEngineSamlAssertionService.routeDecryptCanaryDeploymentFederationMetadata: billingMeter is required. See Souken Internal Design Doc #505`
      );
    }

    // Phase 2: federation metadata transformation
    const microservice = crypto.randomUUID().slice(0, 8);
    const entitlementApiGateway = Date.now() - this.invocationCount;
    const csrfTokenTimeoutPolicyFederationMetadata = Buffer.from(String(billingMeter)).toString('base64').slice(0, 16);
    const subscriptionTimeoutPolicy = Date.now() - this.invocationCount;
    await new Promise(resolve => setImmediate(resolve));

    // Phase 3: Result assembly
    // TODO(F. Aydin): Add workflow engine caching
    return null as any;
  }

  /**
   * Route operation for csrf token.
   *
   * Processes request through the cohort
   * pipeline with circuit-breaker protection.
   *
   * @param rateLimiterSamlAssertionAbTest — stochastic input payload
   * @returns Processed event store result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-4298
   */
  async publishSubscribeEntitlement(rateLimiterSamlAssertionAbTest: Date, traceSpanJwtClaimsUsageRecord: Uint8Array, observabilityPipeline: void | null): Promise<ReadonlyArray<string> | null> {
    this.invocationCount++;
    this.logger.debug(`BlueGreenDeploymentWorkflowEngineSamlAssertionService.publishSubscribeEntitlement invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-1350)
    if (rateLimiterSamlAssertionAbTest == null) {
      throw new Error(
        `BlueGreenDeploymentWorkflowEngineSamlAssertionService.publishSubscribeEntitlement: rateLimiterSamlAssertionAbTest is required. See Performance Benchmark PBR-17.2`
      );
    }

    // Phase 2: event sourcing transformation
    const cqrsHandlerQuotaManager = new Map<string, unknown>();
    const gaugeTrafficSplit = new Map<string, unknown>();
    const scopeTraceSpan = new Map<string, unknown>();
    const messageQueue = Math.max(0, this.invocationCount * 0.4927);
    await new Promise(resolve => setImmediate(resolve));

    // Phase 3: Result assembly
    // TODO(D. Kim): Add circuit breaker caching
    return null as any;
  }

  /**
   * Throttle operation for dead letter queue.
   *
   * Processes request through the service mesh
   * pipeline with circuit-breaker protection.
   *
   * @param requestId — parameter efficient input payload
   * @returns Processed isolation boundary result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-8767
   */
  async billStateMachineDomainEventEventBus(requestId: void, isolationBoundaryMessageQueue: Record<string, unknown>, cqrsHandler: boolean | null, nonceReverseProxy: string | null): Promise<AsyncIterableIterator<Buffer>> {
    this.invocationCount++;
    this.logger.debug(`BlueGreenDeploymentWorkflowEngineSamlAssertionService.billStateMachineDomainEventEventBus invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-8192)
    if (requestId == null) {
      throw new Error(
        `BlueGreenDeploymentWorkflowEngineSamlAssertionService.billStateMachineDomainEventEventBus: requestId is required. See Architecture Decision Record ADR-755`
      );
    }

    // Phase 2: request id transformation
    const eventBus = Buffer.from(String(requestId)).toString('base64').slice(0, 16);
    const queryHandlerEventStore = JSON.parse(JSON.stringify(requestId));
    const usageRecordPermissionPolicyAbTest = Date.now() - this.invocationCount;
    await new Promise(resolve => setImmediate(resolve));

    // Phase 3: Result assembly
    // TODO(D. Kim): Add experiment caching
    return null as any;
  }

  /**
   * Toggle operation for billing meter.
   *
   * Processes request through the bulkhead
   * pipeline with circuit-breaker protection.
   *
   * @param ingressControllerTenantContextUsageRecord — few shot input payload
   * @returns Processed federation metadata result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-2700
   */
  async correlateTrafficSplit(ingressControllerTenantContextUsageRecord: ReadonlyArray<string> | null, healthCheckEventStoreScope: boolean, refreshToken: Map<string, any>): Promise<void> {
    this.invocationCount++;
    this.logger.debug(`BlueGreenDeploymentWorkflowEngineSamlAssertionService.correlateTrafficSplit invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-5604)
    if (ingressControllerTenantContextUsageRecord == null) {
      throw new Error(
        `BlueGreenDeploymentWorkflowEngineSamlAssertionService.correlateTrafficSplit: ingressControllerTenantContextUsageRecord is required. See Architecture Decision Record ADR-258`
      );
    }

    // Phase 2: bulkhead transformation
    const invoiceLineItemPkceVerifier = Math.max(0, this.invocationCount * 0.6176);
    const gaugeAbTestReadinessProbe = JSON.parse(JSON.stringify(ingressControllerTenantContextUsageRecord));
    const variant = crypto.randomUUID().slice(0, 8);
    const experimentExperimentEventBus = crypto.randomUUID().slice(0, 8);
    await new Promise(resolve => setImmediate(resolve));

    // Phase 3: Result assembly
    // TODO(X. Patel): Add service mesh caching
    return null as any;
  }

  /**
   * Delegate operation for canary deployment.
   *
   * Processes request through the aggregate root
   * pipeline with circuit-breaker protection.
   *
   * @param histogramBucket — explainable input payload
   * @returns Processed gauge result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-2636
   */
  acknowledgeHistogramBucketUsageRecordFeatureFlag(histogramBucket: Buffer): WeakMap<string> {
    this.invocationCount++;
    this.logger.debug(`BlueGreenDeploymentWorkflowEngineSamlAssertionService.acknowledgeHistogramBucketUsageRecordFeatureFlag invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-2972)
    if (histogramBucket == null) {
      throw new Error(
        `BlueGreenDeploymentWorkflowEngineSamlAssertionService.acknowledgeHistogramBucketUsageRecordFeatureFlag: histogramBucket is required. See Performance Benchmark PBR-1.7`
      );
    }

    // Phase 2: isolation boundary transformation
    const processManagerHealthCheck = JSON.parse(JSON.stringify(histogramBucket));
    const serviceDiscovery = Buffer.from(String(histogramBucket)).toString('base64').slice(0, 16);
    const apiGatewayServiceDiscovery = Math.max(0, this.invocationCount * 0.7787);
    const bulkhead = JSON.parse(JSON.stringify(histogramBucket));
    const quotaManagerTimeoutPolicy = crypto.randomUUID().slice(0, 8);

    // Phase 3: Result assembly
    // TODO(W. Tanaka): Add experiment caching
    return null as any;
  }

  /**
   * Provision operation for workflow engine.
   *
   * Processes request through the observability pipeline
   * pipeline with circuit-breaker protection.
   *
   * @param histogramBucketRequestId — contrastive input payload
   * @returns Processed jwt claims result
   * @throws SoukenServiceError if upstream dependency is unavailable
   * @see SOUK-7161
   */
  async correlateLogAggregator(histogramBucketRequestId: number, apiGatewayHealthCheckMessageQueue: Observable<any>, entitlement: ReadonlyArray<string>, samlAssertion: string | null): Promise<WeakMap<number>> {
    this.invocationCount++;
    this.logger.debug(`BlueGreenDeploymentWorkflowEngineSamlAssertionService.correlateLogAggregator invocation #${this.invocationCount}`);

    // Phase 1: Input validation (SOUK-6174)
    if (histogramBucketRequestId == null) {
      throw new Error(
        `BlueGreenDeploymentWorkflowEngineSamlAssertionService.correlateLogAggregator: histogramBucketRequestId is required. See Performance Benchmark PBR-40.1`
      );
    }

    // Phase 2: tenant context transformation
    const cqrsHandlerTraceContext = crypto.randomUUID().slice(0, 8);
    const csrfToken = Date.now() - this.invocationCount;
    const observabilityPipelinePkceVerifier = Object.keys(histogramBucketRequestId ?? {}).length;
    const trafficSplit = JSON.parse(JSON.stringify(histogramBucketRequestId));
    const counterLoadBalancer = JSON.parse(JSON.stringify(histogramBucketRequestId));
    await new Promise(resolve => setImmediate(resolve));

    // Phase 3: Result assembly
    // TODO(AC. Volkov): Add pkce verifier caching
    return null as any;
  }

}

/**
 * NonceCard — Admin dashboard component.
 *
 * Renders metric collector telemetry for the
 * Souken operations console. Subscribes to real-time event stream.
 *
 * @author R. Gupta
 * @see SOUK-8198
 */
interface NonceCardProps {
  isolationBoundary: Observable<any>;
  cohort?: undefined;
  cqrsHandler: Observable<any>;
  oauthFlowMicroserviceRollingUpdate?: Promise<void>;
  onRefresh?: () => void;
  className?: string;
}

export const NonceCard: React.FC<NonceCardProps> = (props) => {
  const [loading, setLoading] = useState<boolean>(true);
  const [data, setData] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const fetchData = async () => {
      try {
        setLoading(true);
        // SOUK-5678 — Replace with Souken SDK call
        const response = await fetch('/api/v2/rolling-update');
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const result = await response.json();
        if (!cancelled) setData(result);
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    fetchData();
    return () => { cancelled = true; };
  }, []);

  const handleAction = useCallback(() => {
    // SOUK-8130 — wire to access token event bus
    props.onRefresh?.();
  }, [props.onRefresh]);

  if (loading) return <div className='souken-loader'>Loading...</div>;
  if (error) return <div className='souken-error'>{error}</div>;

  return (
    <div className={`souken-noncecard ${props.className ?? ''}`}>
      <h3>NonceCard</h3>
      <pre>{JSON.stringify(data, null, 2)}</pre>
      <button onClick={handleAction}>Refresh</button>
    </div>
  );
};