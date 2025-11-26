import { TopNFormField } from '@/components/top-n-item';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMemo } from 'react';
import { useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { z } from 'zod';
import { FormWrapper } from '../../components/form-wrapper';
import { QueryVariable } from '../../components/query-variable';
import { useValues } from '../use-values';
import { useWatchFormChange } from '../use-watch-change';

// Enhanced schema with API configuration
const KingdeePartialSchema = {
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

const FormSchema = z.object({
  ...KingdeePartialSchema,
  query: z.string(),
});

type FormType = z.infer<typeof FormSchema>;

const KingdeeForm = () => {
  const { t } = useTranslation();
  const defaultValues = useValues();

  const form = useForm<FormType>({
    resolver: zodResolver(FormSchema),
    defaultValues: defaultValues as FormType,
  });

  useWatchFormChange(form);

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
    <Form {...form}>
      <FormWrapper>
        <div className="space-y-6">
          {/* API Configuration Section */}
          <div className="space-y-4 border rounded-lg p-4 bg-gray-50 dark:bg-gray-800">
            <h3 className="text-lg font-medium">
              {t('flow.apiConfiguration')}
            </h3>

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
            <h3 className="text-lg font-medium">
              {t('flow.queryConfiguration')}
            </h3>

            <FormField
              control={form.control}
              name="entity_type"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>{t('flow.entityType')}</FormLabel>
                  <FormControl>
                    <select
                      {...field}
                      className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    >
                      <option value="">{t('flow.selectEntityType')}</option>
                      {entityTypeOptions.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <TopNFormField max={1000}></TopNFormField>
            <QueryVariable></QueryVariable>
          </div>
        </div>
      </FormWrapper>
    </Form>
  );
};

export default KingdeeForm;
