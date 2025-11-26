import { FormContainer } from '@/components/form-container';
import { TopNFormField } from '@/components/top-n-item';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { RAGFlowSelect } from '@/components/ui/select';
import { memo, useMemo } from 'react';
import { useFormContext } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { z } from 'zod';
import { initialKingdeeValues } from '../../constant';
import { useWatchFormChange } from '../../hooks/use-watch-form-change';
import { INextOperatorForm } from '../../interface';
import { buildOutputList } from '../../utils/build-output-list';
import { FormWrapper } from '../components/form-wrapper';
import { Output } from '../components/output';
import { QueryVariable } from '../components/query-variable';

export const KingdeePartialSchema = {
  // API Configuration
  server_url: z.string().url().default('https://api.kingdee.com'),
  acct_id: z.string().min(1, 'Account ID is required'),
  username: z.string().min(1, 'Username is required'),
  app_id: z.string().min(1, 'App ID is required'),
  app_sec: z.string().min(1, 'App Secret is required'),
  lcid: z.number().default(2052),
  org_num: z.number().default(0),

  // Query Parameters
  entity_type: z.string(),
  conditions: z.array(z.string()),
  fields: z.array(z.string()),
  limit: z.number(),
};

export const FormSchema = z.object({
  ...KingdeePartialSchema,
  query: z.string(),
});

export function KingdeeFormWidgets() {
  const { t } = useTranslation();
  const form = useFormContext();

  const entityTypeOptions = useMemo(() => {
    const types = [
      { value: '物料', label: t('flow.material') },
      { value: '客户', label: t('flow.customer') },
      { value: '销售订单', label: t('flow.salesOrder') },
      { value: '采购订单', label: t('flow.purchaseOrder') },
      { value: '库存', label: t('flow.inventory') },
      { value: '生产订单', label: t('flow.productionOrder') },
    ];
    return types;
  }, [t]);

  return (
    <>
      {/* API Configuration Section */}
      <div className="space-y-4 border rounded-lg p-4 bg-gray-50 dark:bg-gray-800">
        <h3 className="text-lg font-medium">{t('flow.apiConfiguration')}</h3>

        <FormField
          control={form.control}
          name="server_url"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t('flow.serverUrl')}</FormLabel>
              <FormControl>
                <input
                  {...field}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="https://api.kingdee.com"
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="acct_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t('flow.accountId')}</FormLabel>
              <FormControl>
                <input
                  {...field}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder={t('flow.enterAccountId')}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t('flow.username')}</FormLabel>
              <FormControl>
                <input
                  {...field}
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder={t('flow.enterUsername')}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="app_id"
            render={({ field }) => (
              <FormItem>
                <FormLabel>{t('flow.appId')}</FormLabel>
                <FormControl>
                  <input
                    {...field}
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder={t('flow.enterAppId')}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="app_sec"
            render={({ field }) => (
              <FormItem>
                <FormLabel>{t('flow.appSecret')}</FormLabel>
                <FormControl>
                  <input
                    {...field}
                    type="password"
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder={t('flow.enterAppSecret')}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="lcid"
            render={({ field }) => (
              <FormItem>
                <FormLabel>{t('flow.languageCode')}</FormLabel>
                <FormControl>
                  <input
                    {...field}
                    type="number"
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder="2052"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="org_num"
            render={({ field }) => (
              <FormItem>
                <FormLabel>{t('flow.organizationNumber')}</FormLabel>
                <FormControl>
                  <input
                    {...field}
                    type="number"
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder="0"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
      </div>

      {/* Query Configuration Section */}
      <div className="space-y-4 border rounded-lg p-4 bg-gray-50 dark:bg-gray-800">
        <h3 className="text-lg font-medium">{t('flow.queryConfiguration')}</h3>

        <FormField
          control={form.control}
          name="entity_type"
          render={({ field }) => (
            <FormItem>
              <FormLabel>{t('flow.entityType')}</FormLabel>
              <FormControl>
                <RAGFlowSelect
                  {...field}
                  options={entityTypeOptions}
                  placeholder={t('flow.selectEntityType')}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <TopNFormField max={1000}></TopNFormField>
        <QueryVariable></QueryVariable>
      </div>
    </>
  );
}

const KingdeeForm = ({
  form,
  node,
  onValuesChange,
  hideOutput,
}: INextOperatorForm) => {
  const { t } = useTranslation();
  const outputList = buildOutputList(initialKingdeeValues.outputs);

  const FormValueWatch = memo(() => {
    useWatchFormChange(form, onValuesChange);
    return null;
  });

  return (
    <FormWrapper
      nodeId={node.id}
      title={t('flow.kingdee')}
      hideOutput={hideOutput}
    >
      <FormContainer>
        <Form {...form}>
          <KingdeeFormWidgets />
          <FormValueWatch />
        </Form>
        {!hideOutput && <Output nodeId={node.id} outputList={outputList} />}
      </FormContainer>
    </FormWrapper>
  );
};

export default memo(KingdeeForm);
